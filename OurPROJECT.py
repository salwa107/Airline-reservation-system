import bcrypt
import re
import sqlite3
from database import initialize_database, get_connection

class User:
    def __init__(self, username, email, password, contact_number):
        self.__username = username 
        self.__email = email
        self.__password = password
        self.__contact_number = contact_number

    #  getter methods 
    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    @property
    def contact_number(self):
        return self.__contact_number

class Passenger(User):
    def __init__(self, username, email, password, contact_number, passenger_id, age, gender, passport_number, frequent_flyer_status):
        super().__init__(username, email, password, contact_number)
        self.passenger_id = passenger_id
        self.age = age
        self.gender = gender
        self.passport_number = passport_number
        self.frequent_flyer_status = frequent_flyer_status
        self.booking_history = []
        self.loyalty_points = 0

    def sign_up(self, cursor, connection):
        # Validate inputs first
        if not self._validate_email():
            print("Invalid email format!")
            return False
        if not self._validate_password():
            print("Password must be at least 8 characters.")
            return False

        try:
            cursor.execute("SELECT * FROM Passenger WHERE user_name = ?", (self.username,))
            if cursor.fetchone():
                print(f"User {self.username} already exists!")
                return False
            
            password_hash = self._hash_password()
            
            cursor.execute("""
            INSERT INTO Passenger VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.username, self.email, password_hash, self.contact_number,
                self.passenger_id, self.age, self.gender, 
                self.passport_number, self.frequent_flyer_status
            ))
            connection.commit()
            print(f"Passenger {self.username} signed up successfully!")
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            connection.rollback()
            return False

    def sign_in(self, cursor):
        try:
            cursor.execute("SELECT password_hash FROM Passenger WHERE user_name = ?", (self.username,))
            result = cursor.fetchone()
            
            if result and bcrypt.checkpw(self.password.encode(), result[0]):
                print(f"Welcome back, {self.username}!")
                return True
            else:
                print("Invalid username or password.")
                return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    # Password security methods
    def _hash_password(self):
        return bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())

    # Input validation methods
    def _validate_email(self):
        return re.match(r"[^@]+@[^@]+\.[^@]+", self.email)

    def _validate_password(self):
        return len(self.password) >= 8  # Minimum 8 characters

        
    def book_flight(self, flight):
        self.booking_history.append(flight)
        print(f"Flight {flight} booked successfully.")

    def cancel_booking(self, booking_id):
        for booking in self.booking_history:
            if booking['booking_id'] == booking_id:
                self.booking_history.remove(booking)
                print(f"Booking {booking_id} cancelled.")
                return
        print(f"Booking {booking_id} not found.")

    def view_booking_details(self, booking_id):
        for booking in self.booking_history:
            if booking['booking_id'] == booking_id:
                return booking
        print(f"Booking {booking_id} not found.")

    def request_special_assistance(self):
        print("Special assistance requested.")

    def check_in(self):
        print("Checked in successfully.")






class Administrator(User):
    def _init_(self, username, email, password, contact_number, admin_id, role):
        super()._init_(username, email, password, contact_number)
        self.admin_id = admin_id
        self.role = role

    def add_flight(self, flight):
        print(f"Flight {flight} added successfully.")

    def remove_flight(self, flight_id):
        print(f"Flight {flight_id} removed successfully.")

    def manage_airline_operations(self):
        print("Managing airline operations...")

    def assign_gate(self, flight_id, gate_number):
        print(f"Assigned gate {gate_number} to flight {flight_id}.")

    def monitor_flight_status(self, flight_id):
        print(f"Monitoring status of flight {flight_id}.")

    def generate_reports(self):
        print("Generating reports...")

class Flight:
    def __init__(self, flight_id, airline, source, destination, departure_time, arrival_time, available_seats):
        self.flight_id = flight_id
        self.airline = airline
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.available_seats = available_seats

    def update_flight_schedule(self, new_time):
        self.departure_time = new_time

    def check_availability(self):
        return self.available_seats > 0

    def get_flight_info(self):
        return (f"Flight ID: {self.flight_id}, Airline: {self.airline}, Source: {self.source}, "
                f"Destination: {self.destination}, Departure Time: {self.departure_time}, "
                f"Arrival Time: {self.arrival_time}, Available Seats: {self.available_seats}")
class Ticket:
    def __init__(self, ticket_id, passenger, flight, seat_number, ticket_class, price, status):
        self.ticket_id = ticket_id
        self.passenger = passenger
        self.flight = flight
        self.seat_number = seat_number
        self.ticket_class = ticket_class
        self.price = price
        self.status = status

    def generate_ticket(self):
        return (f"Ticket ID: {self.ticket_id}, Passenger: {self.passenger}, Flight: {self.flight.get_flight_info()}, "
                f"Seat Number: {self.seat_number}, Class: {self.ticket_class}, Price: {self.price}, Status: {self.status}")

    def cancel_ticket(self):
        self.status = "Cancelled"
        self.flight.available_seats += 1

    def change_seat(self, new_seat):
        self.seat_number = new_seat


class Booking:
    def __init__(self, booking_id, passenger, flight, ticket, status):
        self.booking_id = booking_id
        self.passenger = passenger
        self.flight = flight
        self.ticket = ticket
        self.status = status

    def confirm_booking(self):
        self.status = "Confirmed"

    def cancel_booking(self):
        self.status = "Cancelled"
        self.ticket.cancel_ticket()

    def modify_booking(self, new_flight):
        self.flight = new_flight
        self.ticket.flight = new_flight

#class FlightReminder(Flight):
    #def check_reminder(self):
        #now = datetime.now()
        #time_until = self.departure_time - now
        #if time_until <= timedelta(hours=3):
            #try:
                #back to payment class, would change the names depending on how it will be named there - Check if Payment class exists and payment is done
                #if Payment.is_payment_done(self.flight_id):
                    #print(f"Reminder: Only {time_until} left until flight {self.flight_id} departure!")
                #else:
                   # print("There's no Reminder for you, please check your payment" )

class Airport:
    
    def __init__(self , airport_id , name , location , avilable_flights):

        self.airport_id = airport_id
        self.name = name
        self.location = location
        self.avilable_flights = avilable_flights

    def list_flights(self):

        print(f"Airport Id:  , {self.airport_id} \n"
              f"Name:  , {self.name}\n"
              f"Location:  , {self.location} \n"
              f"Avilable flights:  , {self.avilable_flights} \n"
              f"")

    def get_airport_info(self):

        return self.airport_id , self.name , self.location , self.avilable_flights #return the info is enought to make get info method

    def check_flight_status(self , fligh_id):
        pass
    


class Airline:
    
    def __init__(self , airline_id , name , fleet_size , destinations , customer_rating):

        self.airline_id = airline_id
        self.name = name
        self.fleet_size = fleet_size
        self.destinations = destinations
        self.customer_rating = customer_rating

    def list_flights_by_airline(self):
        
        print(f"Airline Id: {self.airline_id} \n"
              f"Name: {self.name} \n"
              f"Fleet size: {self.fleet_size} \n"
              f"Destinations: {self.destinations}"
              f"Customer Rating: {self.customer_rating}"
              f"")

    def get_airline_info(self):
            
        return self.airline_id , self.name , self.fleet_size , self.destination , self.customer_rating #return the info is enought to make get info method

    #how about using if conditions for every update data and print all the data with the changed one??
    def update_airline_details(self): 
         pass

class Payment:
    
    def __init__(self, payment_id, passenger, amount, payment_method, status):

        self.payment_id = payment_id
        self.passenger = passenger
        self.amount = amount
        self.payment_method = payment_method
        self.status = status

    def process_payment(self):
        pass

    def refund_payment(self):
        pass

    def view_payment_history(self):
        
        #if all of the data got changed due to a new payment, it will be printed and be saved
        if self.payment_id and self.passenger and self.amount and self.payment_method and self.status:

            print(f"Payment Id: {self.payment_id} \n"
                  f"Passenger: {self.passenger} \n"
                  f"Amount: {self.amount} \n"
                  f"Payment Method: {self.payment_method} \n"
                  f"Status: {self.status}"
                  f"")  

class Baggage:
    def _init_(self, baggage_id, passenger, weight, baggage_fee, status="Checked In"):
        self.baggage_id = baggage_id
        self.passenger = passenger
        self.weight = weight
        self.baggage_fee = baggage_fee
        self.status = status

    def check_baggage_weight(self, max_weight=23):
    
        if self.weight > max_weight:
            print(f"Baggage {self.baggage_id} exceeds the limit! Extra charges may apply.")
            return False
        print(f"Baggage {self.baggage_id} is within the weight limit.")
        return True

    def calculate_fee(self, extra_fee_per_kg=10, max_weight=23):
        """Calculate extra baggage fee if the weight exceeds the limit."""
        if self.weight > max_weight:
            extra_weight = self.weight - max_weight
            self.baggage_fee += extra_weight * extra_fee_per_kg
        return self.baggage_fee

    def update_baggage_status(self, new_status):
        """Update baggage status (Checked In, Loaded, In Transit, Delivered)."""
        self.status = new_status
        print(f"Baggage {self.baggage_id} status updated to {self.status}")


class Seat:
    def _init_(self, seat_id, flight, seat_number, class_type, is_available=True):
        self.seat_id = seat_id
        self.flight = flight
        self.seat_number = seat_number
        self.class_type = class_type
        self.is_available = is_available

    def reserve_seat(self):
        """Reserve the seat if it is available."""
        if self.is_available:
            self.is_available = False
            print(f"Seat {self.seat_number} on flight {self.flight} has been reserved.")
        else:
            print(f"Seat {self.seat_number} is already taken!")

    def release_seat(self):
        """Release the seat, making it available for booking."""
        if not self.is_available:
            self.is_available = True
            print(f"Seat {self.seat_number} on flight {self.flight} is now available.")
        else:
            print(f"Seat {self.seat_number} is already available!")


class LoyaltyProgram:
    def __init__(self, loyalty_id, passenger, points, membership_level):
        self.loyalty_id = loyalty_id
        self.passenger = passenger
        self.points = points
        self.membership_level = membership_level

    def add_points(self, amount):
        self.points += amount

    def redeem_points(self, points):
        if self.points >= points:
            self.points -= points
            return True
        return False





    



def main():
    initialize_database()  

    connection = get_connection()
    cursor = connection.cursor()

    choice = input("Do you want to Sign Up or Sign In? (Enter 'Sign Up' or 'Sign In'): ").strip().lower()

    

    if choice == "sign up":
        print("Welcome to the registration process!")
        username = input("Enter your username: ")
        
        # Email validation loop in main()
        while True:
            email = input("Enter your email: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):  # <-- NOW IN MAIN
                break
            print("Invalid email format! Example: user@example.com")
        
        # Password validation loop
        while True:
            password = input("Enter your password (min 8 chars): ")
            if len(password) >= 8:
                break
            print("Password too short!")

        contact_number = input("Enter your contact number: ")
        passenger_id = input("Enter your passenger ID: ")
        age = int(input("Enter your age: "))
        gender = input("Enter your gender (e.g., Male/Female): ")
        passport_number = input("Enter your passport number: ")
        frequent_flyer_status = input("Enter your frequent flyer status (e.g., Silver/Gold): ")

        new_passenger = Passenger(username, email, password, contact_number, passenger_id, age, gender, passport_number, frequent_flyer_status)
        if new_passenger.sign_up(cursor, connection):
            print("Registration successful!")
        else:
            print("Registration failed.")

    elif choice == "sign in":
        print("\n--- Sign In ---")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        passenger = Passenger(username, "", password, "", 0, 0, "", "", "")
        if passenger.sign_in(cursor):
            print("Proceeding to the dashboard...")
        else:
            print("Invalid credentials.")

    else:
        print("Invalid choice. Please enter 'Sign Up' or 'Sign In'.")

    connection.close()

if __name__ == "__main__":
    main()
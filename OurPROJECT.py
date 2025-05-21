import re
import sqlite3
from abc import ABC, abstractmethod
from database import initialize_database, get_connection
import uuid
conn = sqlite3.connect('project_data.db') 
cursor = conn.cursor()
class User(ABC):
    def __init__(self, username, email, password, contact_number):
        self.__username = username 
        self.__email = email
        self.__password = password
        self.__contact_number = contact_number

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

    @classmethod
    def _validate_email(cls, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    @classmethod
    def _validate_password(cls, password):
        return len(password) >= 8

    @abstractmethod
    def sign_up(self, cursor, connection):
        pass

    @abstractmethod
    def sign_in(self, cursor):
        pass

    @abstractmethod
    def get_table_name(self):
        pass

    @abstractmethod
    def get_extra_fields(self):
        pass


class Passenger(User):
    def __init__(self, username, email, password, contact_number, 
                 passenger_id=None, age=None, gender=None, 
                 passport_number=None, frequent_flyer_status=None):
        super().__init__(username, email, password, contact_number)
        self.passenger_id = passenger_id
        self.age = age
        self.gender = gender
        self.passport_number = passport_number
        self.frequent_flyer_status = frequent_flyer_status
        self.booking_history = []
        self.loyalty_points = 0

    def get_table_name(self):
        return "Passenger"

    def get_extra_fields(self):
        return {
            'passenger_id': self.passenger_id,
            'age': self.age,
            'gender': self.gender,
            'passport_number': self.passport_number,
            'frequent_flyer_status': self.frequent_flyer_status
        }

    def sign_up(self, cursor, connection):
        if not self._validate_email(self.email):
            print("Invalid email format!")
            return False
        if not self._validate_password(self.password):
            print("Password must be at least 8 characters.")
            return False

        try:
            cursor.execute(f"SELECT * FROM {self.get_table_name()} WHERE user_name = ?", 
                         (self.username,))
            if cursor.fetchone():
                print(f"User {self.username} already exists!")
                return False
            
            fields = self.get_extra_fields()
            
            cursor.execute(f"""
                INSERT INTO {self.get_table_name()} 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.username, self.email, self.password, self.contact_number,
                    fields['passenger_id'], fields['age'], fields['gender'], 
                    fields['passport_number'], fields['frequent_flyer_status']
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
            cursor.execute(f"""
                SELECT password FROM {self.get_table_name()} 
                WHERE user_name = ?
                """, (self.username,))
            result = cursor.fetchone()
            
            if result and self.password == result[0]:
                print(f"Welcome back, {self.username}!")
                return True
            else:
                print("Invalid username or password.")
                return False
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    def book_flight(self, flight_id, ticket_id):
        self.booking_history.append(flight_id)

        booking_id = str(uuid.uuid4())  # generate unique booking ID

        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Booking (booking_id, passenger, flight_id, ticket_id)
            VALUES (?, ?, ?, ?)
        """, (booking_id, self.user_name, flight_id, ticket_id))

        conn.commit()
        conn.close()

        print(f"Flight {flight_id} booked successfully! Booking ID: {booking_id}")
    
    


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

class SignInProxy:
    def __init__(self, passenger):
        self.passenger = passenger
        self._authenticated = False

    def sign_in(self, cursor):
        print("[Proxy] Attempting to sign in through proxy...")
        if self.passenger.sign_in(cursor):
            self._authenticated = True
            print("[Proxy] Authentication successful!")
            return True
        else:
            print("[Proxy] Authentication failed!")
            return False

    def is_authenticated(self):
        return self._authenticated

class Administrator(User):
    def __init__(self, username, email, password, contact_number, 
                 admin_id=None, role=None):
        super().__init__(username, email, password, contact_number)
        self.admin_id = admin_id
        self.role = role

    def get_table_name(self):
        return "Administrator"

    def get_extra_fields(self):
        return {
            'admin_id': self.admin_id,
            'role': self.role
        }

    def sign_up(self, cursor, connection):
        if not self._validate_email(self.email):
            print("Invalid email format!")
            return False
        if not self._validate_password(self.password):
            print("Password must be at least 8 characters.")
            return False

        try:
            cursor.execute(f"SELECT * FROM {self.get_table_name()} WHERE user_name = ?", 
                         (self.username,))
            if cursor.fetchone():
                print(f"Administrator {self.username} already exists!")
                return False
            
            fields = self.get_extra_fields()
            
            cursor.execute(f"""
                INSERT INTO {self.get_table_name()} 
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    self.username, self.email, self.password, self.contact_number,
                    fields['admin_id'], fields['role']
                ))
            connection.commit()
            print(f"Administrator {self.username} signed up successfully!")
            return True
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            connection.rollback()
            return False

    def sign_in(self, cursor):
        try:
            cursor.execute(f"""
                SELECT password FROM {self.get_table_name()} 
                WHERE user_name = ?
                """, (self.username,))
            result = cursor.fetchone()
            
            if result and self.password == result[0]:
                print(f"Welcome back Administrator {self.username}!")
                return True
            else:
                print("Invalid username or password.")
                return False
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def flight_exists(self, flight_id, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM Flight WHERE flight_id = ?", (flight_id,))
        return cursor.fetchone() is not None
    def add_flight(self, flight, conn):
        if self.flight_exists(flight.flight_id, conn):
            print(f"Flight {flight.flight_id} already exists.")
            return
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Flight (flight_id, airline, source, destination, departure_time, arrival_time, available_seats)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            flight.flight_id,
            flight.airline,
            flight.source,
            flight.destination,
            flight.departure_time,
            flight.arrival_time,
            flight.available_seats
        ))
        conn.commit()
        print(f"Flight {flight.flight_id} added successfully.")

        


    def manage_airline_operations(self):
        print("Managing airline operations...")

    def assign_gate(self, flight_id, gate_number):
        print(f"Assigned gate {gate_number} to flight {flight_id}.")

    def monitor_flight_status(self, flight_id):
        print(f"Monitoring status of flight {flight_id}.")

    def generate_reports(self):
        print("Generating reports...")


class CrewMember(User):
    def __init__(self, username, email, password, contact_number, 
                 crew_id=None, position=None, airline=None):
        super().__init__(username, email, password, contact_number)
        self.crew_id = crew_id
        self.position = position
        self.airline = airline

    def get_table_name(self):
        return "CrewMember"

    def get_extra_fields(self):
        return {
            'crew_id': self.crew_id,
            'position': self.position,
            'airline': self.airline
        }

    def sign_up(self, cursor, connection):
        if not self._validate_email(self.email):
            print("Invalid email format!")
            return False
        if not self._validate_password(self.password):
            print("Password must be at least 8 characters.")
            return False

        try:
            cursor.execute(f"SELECT * FROM {self.get_table_name()} WHERE user_name = ?", 
                         (self.username,))
            if cursor.fetchone():
                print(f"Crew Member {self.username} already exists!")
                return False
            
            fields = self.get_extra_fields()
            
            cursor.execute(f"""
                INSERT INTO {self.get_table_name()} 
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.username, self.email, self.password, self.contact_number,
                    fields['crew_id'], fields['position'], fields['airline']
                ))
            connection.commit()
            print(f"Crew Member {self.username} signed up successfully!")
            return True
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            connection.rollback()
            return False

    def sign_in(self, cursor):
        try:
            cursor.execute(f"""
                SELECT password FROM {self.get_table_name()} 
                WHERE user_name = ?
                """, (self.username,))
            result = cursor.fetchone()
            
            if result and self.password == result[0]:
                print(f"Welcome back Crew Member {self.username}!")
                return True
            else:
                print("Invalid username or password.")
                return False
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def view_assigned_flights(self, start_date=None, end_date=None):
        print(f"Viewing assigned flights for crew {self.crew_id}")
        return []

    def request_time_off(self, start_date, end_date, reason):
        print(f"Time off requested from {start_date} to {end_date}. Reason: {reason}")
        return True

    def view_crew_schedule(self):
        print(f"Viewing schedule for crew member {self.username}")

    def report_incident(self, flight_id, description):
        print(f"Incident reported for flight {flight_id}: {description}")
        return True

    def check_in_for_flight(self, flight_id):
        print(f"Crew member {self.username} checked in for flight {flight_id}")
        return True



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

    while True:
        print("\nAirline Management System")
        print("1. Passenger")
        print("2. Administrator")
        print("3. Crew Member")
        print("4. Exit")
        
        user_type = input("Select user type (1-4): ").strip()
        
        if user_type == "4":
            print("Exiting... Goodbye!")
            break
            
        if user_type not in ("1", "2", "3"):
            print("Invalid choice. Please try again.")
            continue
            
        action = input("Do you want to Sign Up or Sign In? (Enter 'Sign Up' or 'Sign In'): ").strip().lower()

        if action == "sign up":
            print("\n--- Registration Process ---")

            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password (min 8 chars): ")
            contact_number = input("Enter contact number: ")

            if user_type == "1":  # Passenger
                age = input("Enter age: ")
                gender = input("Enter gender: ")
                passport_number = input("Enter passport number: ")
                frequent_flyer_status = input("Enter frequent flyer status: ")
                user = Passenger(
                    username, email, password, contact_number,
                    passenger_id=None, age=age, gender=gender,
                    passport_number=passport_number,
                    frequent_flyer_status=frequent_flyer_status
                )

            elif user_type == "2":  # Administrator
                admin_id = input("Enter admin ID: ")
                role = input("Enter role: ")
                user = Administrator(
                    username, email, password, contact_number,
                    admin_id=admin_id, role=role
                )

            elif user_type == "3":  # Crew Member
                crew_id = input("Enter crew ID: ")
                position = input("Enter position: ")
                airline = input("Enter airline: ")
                user = CrewMember(
                    username, email, password, contact_number,
                    crew_id=crew_id, position=position, airline=airline
                )

            else:
                print("Unknown user type.")
                continue

            if user.sign_up(cursor, connection):
                print("Registration successful!")
            else:
                print("Registration failed.")

        elif action == "sign in":
            print("\n--- Sign In ---")
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            # Instantiate appropriate user type with minimum fields (email and contact empty since not needed here)
            if user_type == "1":  # Passenger
                real_user = Passenger(username, "", password, "", None, None, None, None, None)
                proxy = SignInProxy(real_user)
                authenticated = proxy.sign_in(cursor)

            elif user_type == "2":  # Administrator
                real_user = Administrator(username, "", password, "", None, None)
                authenticated = real_user.sign_in(cursor)  # No proxy for admin here, but you could add one if you want

            elif user_type == "3":  # Crew Member
                real_user = CrewMember(username, "", password, "", None, None, None)
                authenticated = real_user.sign_in(cursor)  # No proxy here, but can add proxy similarly

            else:
                print("Unknown user type.")
                continue

            if authenticated:
                print(f"Access granted. Welcome {username}!")
                # Here you can add dashboard logic or next steps for the user
            else:
                print("Access denied. Invalid credentials.")

        else:
            print("Invalid choice. Please enter 'Sign Up' or 'Sign In'.")

    connection.close()

if __name__ == "__main__":
    main()

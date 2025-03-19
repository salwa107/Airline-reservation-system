class User:
    def __init__(self, username, email, password, contact_number):
        self.username = username
        self.email = email
        self.password = password
        self.contact_number = contact_number

    def login(self, username, password):
        if self.username == username and self.password == password:
            print("Login successful. Access granted.")
            return True
        else:
            print("Invalid username or password.")
            return False

    def logout(self):
        print("User logged out.")


class Check:
    def verify(self, value1, value2=None):
        if value2 is None:
            return bool(value1)
        return value1 == value2


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

    def book_flight(self, flight):
        self.booking_history.append(flight)
        print(f"Flight {flight.flight_id} booked successfully.")

    def cancel_booking(self, booking_id):
        for booking in self.booking_history:
            if booking.flight_id == booking_id:
                self.booking_history.remove(booking)
                print(f"Booking {booking_id} cancelled.")
                return
        print(f"Booking {booking_id} not found.")

    def view_booking_details(self, booking_id):
        for booking in self.booking_history:
            if booking.flight_id == booking_id:
                return booking.get_flight_info()
        print(f"Booking {booking_id} not found.")
        return None

    def request_special_assistance(self):
        print("Special assistance requested.")

    def check_in(self):
        print("Checked in successfully.")


class Administrator(User):
    def __init__(self, username, email, password, contact_number, admin_id, role):
        super().__init__(username, email, password, contact_number)
        self.admin_id = admin_id
        self.role = role

    def add_flight(self, flight):
        print(f"Flight {flight.flight_id} added successfully.")

    def remove_flight(self, flight_id):
        print(f"Flight {flight_id} removed successfully.")


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


if __name__ == "__main__":
    passenger = Passenger("john_doe", "john@example.com", "secure123", "123-456-7890", "P001", 30, "Male", "A12345678", "Gold")
    admin = Administrator("admin_user", "admin@example.com", "adminpass", "098-765-4321", "A001", "Flight Manager")
    
    username = input("Enter the username: ")
    password = input("Enter your password: ")

    check = Check()
    if check.verify(username, passenger.username) and check.verify(password, passenger.password):
        while True:
            print("\nOptions:")
            print("1. Book a flight")
            print("2. View booking details")
            print("3. Cancel booking")
            print("4. Logout")
            choice = input("Choose an option: ")

            if choice == '1':
                flight = Flight("XY123", "XYZ Airlines", "London", "New York", "10:00 AM", "2:00 PM", 150)
                passenger.book_flight(flight)
            elif choice == '2':
                booking_id = input("Enter booking ID: ")
                print(passenger.view_booking_details(booking_id))
            elif choice == '3':
                booking_id = input("Enter booking ID: ")
                passenger.cancel_booking(booking_id)
            elif choice == '4':
                passenger.logout()
                break
            else:
                print("Invalid choice. Please try again.")

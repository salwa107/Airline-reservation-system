class User:
    def __init__(self, username, email, password, contact_number):
        self.username = username
        self.email = email
        self.password = password
        self.contact_number = contact_number

    def login(self):
        print("User logged in.")

    def logout(self):
        print("User logged out.")


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
    def __init__(self, username, email, password, contact_number, admin_id, role):
        super().__init__(username, email, password, contact_number)
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

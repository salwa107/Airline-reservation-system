import re
import sqlite3
from abc import ABC, abstractmethod
import uuid
from multipledispatch import dispatch

# Database initialization
def initialize_database():
    conn = sqlite3.connect('project_data.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Passenger (
        username TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT,
        contact_number TEXT,
        passenger_id TEXT UNIQUE,
        age INTEGER,
        gender TEXT,
        passport_number TEXT,
        frequent_flyer_status TEXT,
        loyalty_points INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Administrator (
        username TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT,
        contact_number TEXT,
        admin_id TEXT UNIQUE,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CrewMember (
        username TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT,
        contact_number TEXT,
        crew_id TEXT UNIQUE,
        position TEXT,
        airline TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Flight (
        flight_id TEXT PRIMARY KEY,
        airline TEXT,
        source TEXT,
        destination TEXT,
        departure_time TEXT,
        arrival_time TEXT,
        capacity INTEGER,
        available_seats INTEGER,
        base_price REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ticket (
        ticket_id TEXT PRIMARY KEY,
        passenger TEXT,
        flight_id TEXT,
        seat_number TEXT,
        ticket_class TEXT,
        price REAL,
        status TEXT,
        FOREIGN KEY(passenger) REFERENCES Passenger(username),
        FOREIGN KEY(flight_id) REFERENCES Flight(flight_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Booking (
        booking_id TEXT PRIMARY KEY,
        passenger TEXT,
        flight_id TEXT,
        ticket_id TEXT UNIQUE,
        booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Confirmed',
        FOREIGN KEY(passenger) REFERENCES Passenger(username),
        FOREIGN KEY(flight_id) REFERENCES Flight(flight_id),
        FOREIGN KEY(ticket_id) REFERENCES Ticket(ticket_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Payment (
        payment_id TEXT PRIMARY KEY,
        passenger TEXT,
        amount REAL,
        payment_method TEXT,
        status TEXT,
        FOREIGN KEY(passenger) REFERENCES Passenger(username)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Baggage (
        baggage_id TEXT PRIMARY KEY,
        passenger TEXT,
        weight REAL,
        baggage_fee REAL,
        status TEXT,
        FOREIGN KEY(passenger) REFERENCES Passenger(username)
    )
    """)

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect('project_data.db')

# User Abstract Base Class
class User(ABC):
    def __init__(self, username, email, password, contact_number):
        self.__username = username 
        self.__email = email
        self.__password = password
        self.__contact_number = contact_number
#=============property: allaw us to use methods as attributes========== 
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
#==================valid e-mail check if the format is right================
    @classmethod
    def _validate_email(cls, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)
#==================valid password check if the password less than 8 char================
    @classmethod
    def _validate_password(cls, password):
        return len(password) >= 8
#============abstractmethods for over riding==============
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

# Passenger Class
class Passenger(User):
    def __init__(self, username, email, password, contact_number,
                 passenger_id=None, age=None, gender=None,
                 passport_number=None, frequent_flyer_status=None):
        super().__init__(username, email, password, contact_number)
        self.passenger_id = passenger_id or str(uuid.uuid4())
        self.age = age
        self.gender = gender
        self.passport_number = passport_number
        self.frequent_flyer_status = frequent_flyer_status or "None"
        self.loyalty_points = 0
#=============get methods for data==============
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
            print("❌ Invalid email format!")
            return False
        if not self._validate_password(self.password):
            print("❌ Password must be at least 8 characters.")
            return False
#================check if the user already in the data================= 
        try:
            cursor.execute("SELECT * FROM Passenger WHERE username = ? OR email = ?", 
                          (self.username, self.email))
            if cursor.fetchone():
                print(f"⚠️ User {self.username} or email {self.email} already exists!")
                return False

            fields = self.get_extra_fields()
            
            cursor.execute("""
            INSERT INTO Passenger (username, email, password, contact_number, passenger_id,
            age, gender, passport_number, frequent_flyer_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.username, self.email, self.password, self.contact_number,
                fields['passenger_id'], fields['age'], fields['gender'], 
                fields['passport_number'], fields['frequent_flyer_status']
            ))
            connection.commit()
            print(f"✅ Passenger {self.username} signed up successfully!")
            return True

        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            connection.rollback()
            return False

    def sign_in(self, cursor):
    #check if the username and password match
        try:
            cursor.execute("SELECT password FROM Passenger WHERE username = ?", (self.username,))
            result = cursor.fetchone()
            if result and self.password == result[0]:
                print(f"✅ Welcome back, {self.username}!")
                return True
            else:
                print("❌ Invalid username or password.")
                return False
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            return False

    def book_flight(self, flight_id, cursor, connection, ticket_class="Economy"):
        try:
            # Check flight availability and get flight details
            cursor.execute("""
            SELECT available_seats, base_price FROM Flight 
            WHERE flight_id = ? AND available_seats > 0
            """, (flight_id,))
            flight_data = cursor.fetchone()
            
            if not flight_data:
                print("❌ Flight not available or no seats left.")
                return False
                
            available_seats, base_price = flight_data
            
            # Calculate price based on ticket class
            price_multiplier = {
                "Economy": 1.0,
                "Business": 1.5,
                "First": 2.0
            }.get(ticket_class, 1.0)
            
            price = base_price * price_multiplier
            
            # Generate unique IDs
            ticket_id = str(uuid.uuid4())
            booking_id = str(uuid.uuid4())
            
            # Calculate seat number
            seat_row = chr(65 + (100 - available_seats) % 26)  # A-Z rows
            seat_col = (available_seats % 20) + 1  # 1-20 seats per row
            seat_number = f"{seat_row}{seat_col}"
            
            # Start transaction
            connection.execute("BEGIN TRANSACTION")
            
            # Insert ticket
            cursor.execute("""
            INSERT INTO Ticket (ticket_id, passenger, flight_id, seat_number, ticket_class, price, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Confirmed')
            """, (ticket_id, self.username, flight_id, seat_number, ticket_class, price))

            # Insert booking
            cursor.execute("""
            INSERT INTO Booking (booking_id, passenger, flight_id, ticket_id)
            VALUES (?, ?, ?, ?)
            """, (booking_id, self.username, flight_id, ticket_id))

            # Update available seats
            cursor.execute("""
            UPDATE Flight SET available_seats = available_seats - 1 
            WHERE flight_id = ?
            """, (flight_id,))
            
            connection.commit()
            print(f"✈️ Flight {flight_id} booked successfully! Booking ID: {booking_id}")
            print(f"💺 Seat: {seat_number} | 💵 Price: ${price:.2f} ({ticket_class} class)")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Booking failed: {e}")
            connection.rollback()
            return False

    def cancel_booking(self, booking_id, cursor, connection):
        try:
            # Start transaction
            connection.execute("BEGIN TRANSACTION")
            
            # Get booking details and verify passenger ownership
            cursor.execute("""
            SELECT B.flight_id, B.ticket_id 
            FROM Booking B
            JOIN Ticket T ON B.ticket_id = T.ticket_id
            WHERE B.booking_id = ? AND B.passenger = ?
            """, (booking_id, self.username))
            booking = cursor.fetchone()
            
            if not booking:
                print("⚠️ Booking not found or you don't have permission to cancel this booking.")
                connection.rollback()
                return False
                
            flight_id, ticket_id = booking
            
            # Update ticket status to Cancelled
            cursor.execute("""
            UPDATE Ticket SET status = 'Cancelled' 
            WHERE ticket_id = ?
            """, (ticket_id,))
            
            # Delete the booking record
            cursor.execute("""
            DELETE FROM Booking 
            WHERE booking_id = ?
            """, (booking_id,))
            
            # Increment available seats
            cursor.execute("""
            UPDATE Flight SET available_seats = available_seats + 1 
            WHERE flight_id = ?
            """, (flight_id,))
            
            connection.commit()
            print(f"❌ Booking {booking_id} cancelled successfully.")
            print(f"🔄 Seat for flight {flight_id} has been released.")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error cancelling booking: {e}")
            connection.rollback()
            return False

    def view_booking_details(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            SELECT B.booking_id, F.flight_id, F.source, F.destination, 
                   F.departure_time, T.seat_number, T.ticket_class, T.price, T.status
            FROM Booking B
            JOIN Ticket T ON B.ticket_id = T.ticket_id
            JOIN Flight F ON B.flight_id = F.flight_id
            WHERE B.passenger = ?
            """, (self.username,))
            
            bookings = cursor.fetchall()
            
            if not bookings:
                print("You have no bookings yet.")
                return
                
            print("\n📋 Your Bookings:")
            for booking in bookings:
                print(f"\nBooking ID: {booking[0]}")
                print(f"Flight: {booking[1]} ({booking[2]} → {booking[3]})")
                print(f"Departure: {booking[4]} | Seat: {booking[5]} ({booking[6]})")
                print(f"Price: ${booking[7]:.2f} | Status: {booking[8]}")
                
        except sqlite3.Error as e:
            print(f"❌ Error retrieving bookings: {e}")
        finally:
            conn.close()

    def request_special_assistance(self):
        print("\nSpecial Assistance Request")
        print("Please describe your special needs:")
        needs = input("> ")
        print("✅ Your request has been submitted. We'll contact you soon.")

    def check_in(self, flight_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            SELECT T.ticket_id, T.seat_number, T.status
            FROM Ticket T
            JOIN Booking B ON T.ticket_id = B.ticket_id
            WHERE B.passenger = ? AND B.flight_id = ?
            """, (self.username, flight_id))
            
            ticket = cursor.fetchone()
            
            if not ticket:
                print("❌ No booking found for this flight.")
                return False
                
            ticket_id, seat_number, status = ticket
            
            if status == "Cancelled":
                print("❌ This booking has been cancelled.")
                return False
                
            print(f"✅ Check-in successful for Flight {flight_id}")
            print(f"Your seat number is: {seat_number}")
            print("Please proceed to the boarding gate with your boarding pass.")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error during check-in: {e}")
            return False
        finally:
            conn.close()

# SignInProxy Class
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

# Administrator Class
class Administrator(User):
    def __init__(self, username, email, password, contact_number, 
                 admin_id=None, role=None):
        super().__init__(username, email, password, contact_number)
        self.admin_id = admin_id or str(uuid.uuid4())
        self.role = role or "System Admin"

    def get_table_name(self):
        return "Administrator"

    def get_extra_fields(self):
        return {
            'admin_id': self.admin_id,
            'role': self.role
        }

    def sign_up(self, cursor, connection):
        if not self._validate_email(self.email):
            print("❌ Invalid email format!")
            return False
        if not self._validate_password(self.password):
            print("❌ Password must be at least 8 characters.")
            return False

        try:
            cursor.execute(f"SELECT * FROM {self.get_table_name()} WHERE username = ? OR email = ?", 
                         (self.username, self.email))
            if cursor.fetchone():
                print(f"⚠️ Administrator {self.username} or email {self.email} already exists!")
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
            print(f"✅ Administrator {self.username} signed up successfully!")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            connection.rollback()
            return False

    def sign_in(self, cursor):
        try:
            cursor.execute(f"""
                SELECT password FROM {self.get_table_name()} 
                WHERE username = ?
                """, (self.username,))
            result = cursor.fetchone()
            
            if result and self.password == result[0]:
                print(f"✅ Welcome back Administrator {self.username}!")
                return True
            else:
                print("❌ Invalid username or password.")
                return False
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            return False

    def flight_exists(self, flight_id, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM Flight WHERE flight_id = ?", (flight_id,))
        return cursor.fetchone() is not None

    def add_flight(self, flight, conn):
        if self.flight_exists(flight.flight_id, conn):
            print(f"❌ Flight {flight.flight_id} already exists.")
            return False
            
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Flight (flight_id, airline, source, destination, 
                                  departure_time, arrival_time, capacity, 
                                  available_seats, base_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                flight.flight_id,
                flight.airline,
                flight.source,
                flight.destination,
                flight.departure_time,
                flight.arrival_time,
                flight.capacity,
                flight.available_seats,
                flight.base_price
            ))
            conn.commit()
            print(f"✅ Flight {flight.flight_id} added successfully.")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error adding flight: {e}")
            conn.rollback()
            return False

    def remove_flight(self, flight_id, conn):
        if not self.flight_exists(flight_id, conn):
            print(f"❌ Flight {flight_id} does not exist.")
            return False
            
        cursor = conn.cursor()
        try:
            # Check if there are any bookings for this flight
            cursor.execute("SELECT 1 FROM Booking WHERE flight_id = ?", (flight_id,))
            if cursor.fetchone():
                print("⚠️ Cannot remove flight with active bookings.")
                return False
                
            cursor.execute("DELETE FROM Flight WHERE flight_id = ?", (flight_id,))
            conn.commit()
            print(f"✅ Flight {flight_id} removed successfully.")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error removing flight: {e}")
            conn.rollback()
            return False

    def manage_airline_operations(self):
        print("Managing airline operations...")

    def assign_gate(self, flight_id, gate_number):
        print(f"Assigned gate {gate_number} to flight {flight_id}.")

    def monitor_flight_status(self, flight_id):
        print(f"Monitoring status of flight {flight_id}.")
#===========overloading============
    @dispatch()
    def generate_reports(self):
            print("Generating general reports...")

    @dispatch(str)
    def generate_reports(self, report_type):
            print(f"Generating report of type: {report_type}")

    @dispatch(str, int)
    def generate_reports(self, report_type, year):
            print(f"Generating {report_type} report for the year {year}")


# CrewMember Class
class CrewMember(User):
    def __init__(self, username, email, password, contact_number, 
                 crew_id=None, position=None, airline=None):
        super().__init__(username, email, password, contact_number)
        self.crew_id = crew_id or str(uuid.uuid4())
        self.position = position or "Flight Attendant"
        self.airline = airline or "Generic Airlines"

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
            print("❌ Invalid email format!")
            return False
        if not self._validate_password(self.password):
            print("❌ Password must be at least 8 characters.")
            return False

        try:
            cursor.execute(f"SELECT * FROM {self.get_table_name()} WHERE username = ? OR email = ?", 
                         (self.username, self.email))
            if cursor.fetchone():
                print(f"⚠️ Crew Member {self.username} or email {self.email} already exists!")
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
            print(f"✅ Crew Member {self.username} signed up successfully!")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            connection.rollback()
            return False

    def sign_in(self, cursor):
        try:
            cursor.execute(f"""
                SELECT password FROM {self.get_table_name()} 
                WHERE username = ?
                """, (self.username,))
            result = cursor.fetchone()
            
            if result and self.password == result[0]:
                print(f"✅ Welcome back Crew Member {self.username}!")
                return True
            else:
                print("❌ Invalid username or password.")
                return False
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            return False

    def view_assigned_flights(self, start_date=None, end_date=None):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT F.flight_id, F.source, F.destination, 
                   F.departure_time, F.arrival_time
            FROM Flight F
            WHERE F.airline = ?
            """
            params = [self.airline]
            
            if start_date and end_date:
                query += " AND F.departure_time BETWEEN ? AND ?"
                params.extend([start_date, end_date])
                
            cursor.execute(query, params)
            flights = cursor.fetchall()
            
            if not flights:
                print("No assigned flights found.")
                return []
                
            print("\n✈️ Your Assigned Flights:")
            for flight in flights:
                print(f"\nFlight {flight[0]}: {flight[1]} → {flight[2]}")
                print(f"Departure: {flight[3]} | Arrival: {flight[4]}")
                
            return flights
            
        except sqlite3.Error as e:
            print(f"❌ Error retrieving flights: {e}")
            return []
        finally:
            conn.close()

    def request_time_off(self, start_date, end_date, reason):
        print(f"⏳ Time off requested from {start_date} to {end_date}. Reason: {reason}")
        return True

    def view_crew_schedule(self):
        return self.view_assigned_flights()

    def report_incident(self, flight_id, description):
        print(f"⚠️ Incident reported for flight {flight_id}: {description}")
        return True

    def check_in_for_flight(self, flight_id):
        print(f"✅ Crew member {self.username} checked in for flight {flight_id}")
        return True

# Flight Class
class Flight:
    def __init__(self, flight_id, airline, source, destination, 
                 departure_time, arrival_time, capacity, available_seats=None, base_price=0.0):
        self.flight_id = flight_id
        self.airline = airline
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.capacity = capacity
        self.available_seats = available_seats if available_seats is not None else capacity
        self.base_price = base_price

    def update_flight_schedule(self, new_time):
        self.departure_time = new_time
        conn = get_connection()
        try:
            conn.execute("""
            UPDATE Flight SET departure_time = ? 
            WHERE flight_id = ?
            """, (new_time, self.flight_id))
            conn.commit()
            print("Flight schedule updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating flight schedule: {e}")
        finally:
            conn.close()

    def check_availability(self):
        return self.available_seats > 0

    def get_flight_info(self):
        return (f"Flight ID: {self.flight_id}, Airline: {self.airline}, Source: {self.source}, "
                f"Destination: {self.destination}, Departure Time: {self.departure_time}, "
                f"Arrival Time: {self.arrival_time}, Available Seats: {self.available_seats}/{self.capacity}")

# Ticket Class
class Ticket:
    def __init__(self, ticket_id, passenger, flight_id, seat_number, 
                 ticket_class, price, status="Confirmed"):
        self.ticket_id = ticket_id
        self.passenger = passenger
        self.flight_id = flight_id
        self.seat_number = seat_number
        self.ticket_class = ticket_class
        self.price = price
        self.status = status

    def generate_ticket(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT source, destination, departure_time 
            FROM Flight WHERE flight_id = ?
            """, (self.flight_id,))
            flight_info = cursor.fetchone()
            
            if flight_info:
                source, destination, departure = flight_info
                return (f"Ticket ID: {self.ticket_id}\n"
                        f"Passenger: {self.passenger}\n"
                        f"Flight: {self.flight_id} ({source} → {destination})\n"
                        f"Departure: {departure}\n"
                        f"Seat Number: {self.seat_number}\n"
                        f"Class: {self.ticket_class}\n"
                        f"Price: ${self.price:.2f}\n"
                        f"Status: {self.status}")
            return "Flight information not found."
        except sqlite3.Error as e:
            return f"Error retrieving ticket information: {e}"
        finally:
            conn.close()

    def cancel_ticket(self):
        conn = get_connection()
        try:
            conn.execute("""
            UPDATE Ticket SET status = 'Cancelled' 
            WHERE ticket_id = ?
            """, (self.ticket_id,))
            
            conn.execute("""
            UPDATE Flight SET available_seats = available_seats + 1 
            WHERE flight_id = ?
            """, (self.flight_id,))
            
            conn.commit()
            self.status = "Cancelled"
            print("Ticket cancelled successfully.")
        except sqlite3.Error as e:
            print(f"Error cancelling ticket: {e}")
        finally:
            conn.close()

    def change_seat(self, new_seat):
        conn = get_connection()
        try:
            conn.execute("""
            UPDATE Ticket SET seat_number = ? 
            WHERE ticket_id = ?
            """, (new_seat, self.ticket_id))
            conn.commit()
            self.seat_number = new_seat
            print("Seat changed successfully.")
        except sqlite3.Error as e:
            print(f"Error changing seat: {e}")
        finally:
            conn.close()

# Booking Class
class Booking:
    def __init__(self, booking_id, passenger, flight_id, ticket_id, status="Confirmed"):
        self.booking_id = booking_id
        self.passenger = passenger
        self.flight_id = flight_id
        self.ticket_id = ticket_id
        self.status = status

    def confirm_booking(self):
        conn = get_connection()
        try:
            conn.execute("""
            UPDATE Booking SET status = 'Confirmed' 
            WHERE booking_id = ?
            """, (self.booking_id,))
            conn.commit()
            self.status = "Confirmed"
            print("Booking confirmed.")
        except sqlite3.Error as e:
            print(f"Error confirming booking: {e}")
        finally:
            conn.close()

    def cancel_booking(self):
        conn = get_connection()
        try:
            # Get ticket ID first
            cursor = conn.cursor()
            cursor.execute("""
            SELECT ticket_id FROM Booking 
            WHERE booking_id = ?
            """, (self.booking_id,))
            ticket_id = cursor.fetchone()[0]
            
            # Cancel the booking
            conn.execute("""
            UPDATE Booking SET status = 'Cancelled' 
            WHERE booking_id = ?
            """, (self.booking_id,))
            
            # Cancel the associated ticket
            ticket = Ticket(ticket_id, self.passenger, self.flight_id, "", "", 0)
            ticket.cancel_ticket()
            
            conn.commit()
            self.status = "Cancelled"
            print("Booking cancelled successfully.")
        except sqlite3.Error as e:
            print(f"Error cancelling booking: {e}")
        finally:
            conn.close()

# Airport Class
class Airport:
    def __init__(self, airport_id, name, location):
        self.airport_id = airport_id
        self.name = name
        self.location = location

    def list_flights(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT flight_id, airline, destination, departure_time, available_seats
            FROM Flight 
            WHERE source = ?
            ORDER BY departure_time
            """, (self.airport_id,))
            
            flights = cursor.fetchall()
            
            print(f"\n✈️ Flights from {self.name} ({self.location}):")
            for flight in flights:
                print(f"\nFlight {flight[0]} by {flight[1]}")
                print(f"To: {flight[2]} | Departure: {flight[3]}")
                print(f"Available Seats: {flight[4]}")
                
            return flights
        except sqlite3.Error as e:
            print(f"Error listing flights: {e}")
            return []
        finally:
            conn.close()

    def get_airport_info(self):
        return f"{self.name} ({self.airport_id}) - {self.location}"

# Airline Class
class Airline:
    def __init__(self, airline_id, name, fleet_size=0):
        self.airline_id = airline_id
        self.name = name
        self.fleet_size = fleet_size

    def list_flights_by_airline(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT flight_id, source, destination, departure_time, available_seats
            FROM Flight 
            WHERE airline = ?
            ORDER BY departure_time
            """, (self.airline_id,))
            
            flights = cursor.fetchall()
            
            print(f"\n✈️ Flights by {self.name}:")
            for flight in flights:
                print(f"\nFlight {flight[0]}: {flight[1]} → {flight[2]}")
                print(f"Departure: {flight[3]} | Available Seats: {flight[4]}")
                
            return flights
        except sqlite3.Error as e:
            print(f"Error listing flights: {e}")
            return []
        finally:
            conn.close()

    def get_airline_info(self):
        return f"{self.name} (ID: {self.airline_id}) - Fleet Size: {self.fleet_size}"

# Payment Class
class Payment:
    def __init__(self, payment_id, passenger, amount, payment_method, status="Pending"):
        self.payment_id = payment_id
        self.passenger = passenger
        self.amount = amount
        self.payment_method = payment_method
        self.status = status

    def process_payment(self):
        conn = get_connection()
        try:
            conn.execute("""
            INSERT INTO Payment (payment_id, passenger, amount, payment_method, status)
            VALUES (?, ?, ?, ?, ?)
            """, (
                self.payment_id,
                self.passenger,
                self.amount,
                self.payment_method,
                "Completed"
            ))
            conn.commit()
            self.status = "Completed"
            print("Payment processed successfully.")
            return True
        except sqlite3.Error as e:
            print(f"Error processing payment: {e}")
            return False
        finally:
            conn.close()

    def refund_payment(self):
        conn = get_connection()
        try:
            conn.execute("""
            UPDATE Payment SET status = 'Refunded' 
            WHERE payment_id = ?
            """, (self.payment_id,))
            conn.commit()
            self.status = "Refunded"
            print("Payment refunded successfully.")
            return True
        except sqlite3.Error as e:
            print(f"Error refunding payment: {e}")
            return False
        finally:
            conn.close()

    def view_payment_history(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT payment_id, amount, payment_method, status 
            FROM Payment 
            WHERE passenger = ?
            ORDER BY status DESC
            """, (self.passenger,))
            
            payments = cursor.fetchall()
            
            print(f"\n💰 Payment History for {self.passenger}:")
            for payment in payments:
                print(f"\nPayment ID: {payment[0]}")
                print(f"Amount: ${payment[1]:.2f} | Method: {payment[2]}")
                print(f"Status: {payment[3]}")
                
            return payments
        except sqlite3.Error as e:
            print(f"Error retrieving payment history: {e}")
            return []
        finally:
            conn.close()

# Baggage Class
class Baggage:
    def __init__(self, baggage_id, passenger, weight, baggage_fee=0, status="Checked In"):
        self.baggage_id = baggage_id
        self.passenger = passenger
        self.weight = weight
        self.baggage_fee = baggage_fee
        self.status = status

    def check_baggage_weight(self, max_weight=23):
        if self.weight > max_weight:
            print(f"⚠️ Baggage {self.baggage_id} exceeds the limit! Extra charges may apply.")
            return False
        print(f"✅ Baggage {self.baggage_id} is within the weight limit.")
        return True

    def calculate_fee(self, extra_fee_per_kg=10, max_weight=23):
        if self.weight > max_weight:
            extra_weight = self.weight - max_weight
            self.baggage_fee += extra_weight * extra_fee_per_kg
            conn = get_connection()
            try:
                conn.execute("""
                UPDATE Baggage SET baggage_fee = ?, status = 'Fee Pending'
                WHERE baggage_id = ?
                """, (self.baggage_fee, self.baggage_id))
                conn.commit()
                self.status = "Fee Pending"
            except sqlite3.Error as e:
                print(f"Error updating baggage fee: {e}")
            finally:
                conn.close()
        return self.baggage_fee

    def update_baggage_status(self, new_status):
        conn = get_connection()
        try:
            conn.execute("""
            UPDATE Baggage SET status = ?
            WHERE baggage_id = ?
            """, (new_status, self.baggage_id))
            conn.commit()
            self.status = new_status
            print(f"Baggage {self.baggage_id} status updated to {new_status}")
        except sqlite3.Error as e:
            print(f"Error updating baggage status: {e}")
        finally:
            conn.close()

def main():
    # Initialize database when the program starts
    initialize_database()
    
    print("="*50)
    print("🛫 AIRLINE MANAGEMENT SYSTEM 🛬")
    print("="*50)
    
    while True:
        print("\nPlease select your role:")
        print("1. Passenger")
        print("2. Administrator")
        print("3. Crew Member")
        print("4. Exit")
        
        role_choice = input("Enter your choice (1-4): ")
        
        if role_choice == "1":
            passenger_menu()
        elif role_choice == "2":
            admin_menu()
        elif role_choice == "3":
            crew_menu()
        elif role_choice == "4":
            print("Thank you for using the Airline Management System. Goodbye! ✈️")
            break
        else:
            print("Invalid choice! Please try again.")

def passenger_menu():
    print("\n=== PASSENGER PORTAL ===")
    print("1. Sign Up")
    print("2. Sign In")
    print("3. Return to Main Menu")
    
    choice = input("Enter your choice (1-3): ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if choice == "1":
        # Passenger Sign Up
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        contact_number = input("Enter contact number: ")
        age = int(input("Enter age: "))
        gender = input("Enter gender: ")
        passport_number = input("Enter passport number: ")
        
        passenger = Passenger(username, email, password, contact_number, 
                             None, age, gender, passport_number)
        if passenger.sign_up(cursor, conn):
            logged_in_passenger_menu(passenger)
    
    elif choice == "2":
        # Passenger Sign In
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        passenger = Passenger(username, "", password, "")
        proxy = SignInProxy(passenger)
        
        if proxy.sign_in(cursor):
            # Retrieve complete passenger information
            cursor.execute("""
            SELECT email, contact_number, passenger_id, age, gender, 
                   passport_number, frequent_flyer_status, loyalty_points
            FROM Passenger WHERE username = ?
            """, (username,))
            
            data = cursor.fetchone()
            if data:
                passenger = Passenger(username, data[0], password, data[1], 
                                     data[2], data[3], data[4], data[5])
                passenger.frequent_flyer_status = data[6]
                logged_in_passenger_menu(passenger)
    
    elif choice == "3":
        return
    
    else:
        print("Invalid choice!")
    
    conn.close()

def logged_in_passenger_menu(passenger):
    while True:
        print(f"\n=== Welcome, {passenger.username}! ===")
        print("1. Search and Book Flights")
        print("2. View My Bookings")
        print("3. Cancel a Booking")
        print("4. Check-in for a Flight")
        print("5. Request Special Assistance")
        print("6. Logout")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            search_and_book_flight(passenger)
        elif choice == "2":
            passenger.view_booking_details()
        elif choice == "3":
            booking_id = input("Enter booking ID to cancel: ")
            conn = get_connection()
            passenger.cancel_booking(booking_id, conn.cursor(), conn)
            conn.close()
        elif choice == "4":
            flight_id = input("Enter flight ID to check-in: ")
            passenger.check_in(flight_id)
        elif choice == "5":
            passenger.request_special_assistance()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

def search_and_book_flight(passenger):
    print("\n=== FLIGHT SEARCH ===")
    source = input("Enter departure city/airport: ")
    destination = input("Enter destination city/airport: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        SELECT flight_id, airline, departure_time, arrival_time, 
               available_seats, base_price
        FROM Flight
        WHERE source LIKE ? AND destination LIKE ? AND available_seats > 0
        """, (f"%{source}%", f"%{destination}%"))
        
        flights = cursor.fetchall()
        
        if not flights:
            print("No flights found for your search criteria.")
            return
            
        print("\nAvailable Flights:")
        for i, flight in enumerate(flights):
            print(f"{i+1}. Flight {flight[0]} by {flight[1]}")
            print(f"   {source} → {destination}")
            print(f"   Departure: {flight[2]} | Arrival: {flight[3]}")
            print(f"   Available Seats: {flight[4]} | Base Price: ${flight[5]:.2f}")
            print("---")
        
        flight_choice = input("Enter flight number to book (or 0 to cancel): ")
        if flight_choice == "0":
            return
            
        flight_index = int(flight_choice) - 1
        if 0 <= flight_index < len(flights):
            selected_flight = flights[flight_index]
            flight_id = selected_flight[0]
            
            print("\nSelect ticket class:")
            print("1. Economy")
            print("2. Business")
            print("3. First Class")
            
            class_choice = input("Enter your choice (1-3): ")
            ticket_class = {
                "1": "Economy",
                "2": "Business",
                "3": "First"
            }.get(class_choice, "Economy")
            
            if passenger.book_flight(flight_id, cursor, conn, ticket_class):
                # Calculate price for display
                base_price = selected_flight[5]
                price_multiplier = {
                    "Economy": 1.0,
                    "Business": 1.5,
                    "First": 2.0
                }.get(ticket_class, 1.0)
                
                price = base_price * price_multiplier
                
                # Create a payment for the booking
                payment_id = str(uuid.uuid4())
                payment = Payment(payment_id, passenger.username, price, "Credit Card")
                
                print("\n=== PAYMENT ===")
                print(f"Total Amount: ${price:.2f}")
                print("1. Credit Card")
                print("2. Debit Card")
                print("3. PayPal")
                
                payment_choice = input("Select payment method (1-3): ")
                payment_method = {
                    "1": "Credit Card",
                    "2": "Debit Card",
                    "3": "PayPal"
                }.get(payment_choice, "Credit Card")
                
                payment.payment_method = payment_method
                if payment.process_payment():
                    print("✅ Flight booked and payment processed successfully!")
                    
                    # Ask if user wants to add baggage
                    add_baggage = input("Do you want to add baggage? (y/n): ").lower()
                    if add_baggage == 'y':
                        baggage_id = str(uuid.uuid4())
                        weight = float(input("Enter baggage weight in kg: "))
                        
                        baggage = Baggage(baggage_id, passenger.username, weight)
                        
                        if not baggage.check_baggage_weight():
                            print(f"Excess baggage fee: ${baggage.calculate_fee():.2f}")
                            pay_fee = input("Pay excess baggage fee? (y/n): ").lower()
                            if pay_fee == 'y':
                                baggage_payment_id = str(uuid.uuid4())
                                baggage_payment = Payment(baggage_payment_id, 
                                                         passenger.username, 
                                                         baggage.baggage_fee, 
                                                         payment_method)
                                if baggage_payment.process_payment():
                                    baggage.status = "Checked In"
                                    print("✅ Baggage fee paid successfully!")
                        
                        # Insert baggage into database
                        conn.execute("""
                        INSERT INTO Baggage (baggage_id, passenger, weight, baggage_fee, status)
                        VALUES (?, ?, ?, ?, ?)
                        """, (baggage_id, passenger.username, weight, 
                             baggage.baggage_fee, baggage.status))
                        conn.commit()
        else:
            print("Invalid flight selection.")
            
    except sqlite3.Error as e:
        print(f"Error searching flights: {e}")
    finally:
        conn.close()

def admin_menu():
    print("\n=== ADMINISTRATOR PORTAL ===")
    print("1. Sign Up")
    print("2. Sign In")
    print("3. Return to Main Menu")
    
    choice = input("Enter your choice (1-3): ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if choice == "1":
        # Admin Sign Up
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        contact_number = input("Enter contact number: ")
        role = input("Enter role (default: System Admin): ") or "System Admin"
        
        admin = Administrator(username, email, password, contact_number, 
                             None, role)
        if admin.sign_up(cursor, conn):
            logged_in_admin_menu(admin)
    
    elif choice == "2":
        # Admin Sign In
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        admin = Administrator(username, "", password, "")
        
        if admin.sign_in(cursor):
            # Retrieve complete admin information
            cursor.execute("""
            SELECT email, contact_number, admin_id, role
            FROM Administrator WHERE username = ?
            """, (username,))
            
            data = cursor.fetchone()
            if data:
                admin = Administrator(username, data[0], password, data[1], 
                                    data[2], data[3])
                logged_in_admin_menu(admin)
    
    elif choice == "3":
        return
    
    else:
        print("Invalid choice!")
    
    conn.close()

def logged_in_admin_menu(admin):
    while True:
        print(f"\n=== Welcome Administrator {admin.username}! ===")
        print("1. Add New Flight")
        print("2. Remove Flight")
        print("3. Assign Gate")
        print("4. Monitor Flight Status")
        print("5. Generate Reports")
        print("6. Logout")
        
        choice = input("Enter your choice (1-6): ")
        
        conn = get_connection()
        
        if choice == "1":
            flight_id = input("Enter flight ID: ")
            airline = input("Enter airline: ")
            source = input("Enter source airport: ")
            destination = input("Enter destination airport: ")
            departure_time = input("Enter departure time (YYYY-MM-DD HH:MM): ")
            arrival_time = input("Enter arrival time (YYYY-MM-DD HH:MM): ")
            capacity = int(input("Enter capacity: "))
            base_price = float(input("Enter base price: "))
            
            flight = Flight(flight_id, airline, source, destination, 
                           departure_time, arrival_time, capacity, capacity, base_price)
            admin.add_flight(flight, conn)
        
        elif choice == "2":
            flight_id = input("Enter flight ID to remove: ")
            admin.remove_flight(flight_id, conn)
        
        elif choice == "3":
            flight_id = input("Enter flight ID: ")
            gate_number = input("Enter gate number: ")
            admin.assign_gate(flight_id, gate_number)
        
        elif choice == "4":
            flight_id = input("Enter flight ID to monitor: ")
            admin.monitor_flight_status(flight_id)
        
        elif choice == "5":
            admin.generate_reports()
        
        elif choice == "6":
            print("Logging out...")
            break
        
        else:
            print("Invalid choice!")
        
        conn.close()

def crew_menu():
    print("\n=== CREW MEMBER PORTAL ===")
    print("1. Sign Up")
    print("2. Sign In")
    print("3. Return to Main Menu")
    
    choice = input("Enter your choice (1-3): ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if choice == "1":
        # Crew Sign Up
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        contact_number = input("Enter contact number: ")
        position = input("Enter position (default: Flight Attendant): ") or "Flight Attendant"
        airline = input("Enter airline: ")
        
        crew = CrewMember(username, email, password, contact_number, 
                         None, position, airline)
        if crew.sign_up(cursor, conn):
            logged_in_crew_menu(crew)
    
    elif choice == "2":
        # Crew Sign In
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        crew = CrewMember(username, "", password, "")
        
        if crew.sign_in(cursor):
            # Retrieve complete crew information
            cursor.execute("""
            SELECT email, contact_number, crew_id, position, airline
            FROM CrewMember WHERE username = ?
            """, (username,))
            
            data = cursor.fetchone()
            if data:
                crew = CrewMember(username, data[0], password, data[1], 
                                 data[2], data[3], data[4])
                logged_in_crew_menu(crew)
    
    elif choice == "3":
        return
    
    else:
        print("Invalid choice!")
    
    conn.close()

def logged_in_crew_menu(crew):
    while True:
        print(f"\n=== Welcome {crew.position} {crew.username}! ===")
        print("1. View Assigned Flights")
        print("2. Check-in for Flight")
        print("3. View Schedule")
        print("4. Request Time Off")
        print("5. Report Incident")
        print("6. Logout")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            start_date = input("Enter start date (YYYY-MM-DD) or leave blank for all: ")
            end_date = input("Enter end date (YYYY-MM-DD) or leave blank for all: ")
            crew.view_assigned_flights(start_date, end_date)
        
        elif choice == "2":
            flight_id = input("Enter flight ID to check in: ")
            crew.check_in_for_flight(flight_id)
        
        elif choice == "3":
            crew.view_crew_schedule()
        
        elif choice == "4":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            reason = input("Enter reason for time off: ")
            crew.request_time_off(start_date, end_date, reason)
        
        elif choice == "5":
            flight_id = input("Enter flight ID: ")
            description = input("Describe the incident: ")
            crew.report_incident(flight_id, description)
        
        elif choice == "6":
            print("Logging out...")
            break
        
        else:
            print("Invalid choice!")

# Sample data for demonstration purposes
def add_sample_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check if we already have sample data
        cursor.execute("SELECT COUNT(*) FROM Flight")
        if cursor.fetchone()[0] > 0:
            return  # Data already exists
        
        # Add sample flights
        flights = [
            Flight("BA123", "British Airways", "London", "New York", "2025-06-01 08:00", "2025-06-01 11:30", 200, 180, 350.0),
            Flight("EK456", "Emirates", "Dubai", "London", "2025-06-02 14:00", "2025-06-02 19:45", 350, 320, 420.0),
            Flight("QF789", "Qantas", "Sydney", "Singapore", "2025-06-03 22:00", "2025-06-04 04:30", 280, 250, 380.0),
            Flight("SQ246", "Singapore Airlines", "Singapore", "Tokyo", "2025-06-05 10:30", "2025-06-05 18:00", 300, 270, 290.0),
            Flight("LH802", "Lufthansa", "Frankfurt", "Cairo", "2025-06-10 12:15", "2025-06-10 17:30", 250, 200, 310.0)
        ]
        
        for flight in flights:
            cursor.execute("""
            INSERT INTO Flight (flight_id, airline, source, destination, departure_time, 
                               arrival_time, capacity, available_seats, base_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                flight.flight_id, flight.airline, flight.source, flight.destination,
                flight.departure_time, flight.arrival_time, flight.capacity,
                flight.available_seats, flight.base_price
            ))
        
        # Add sample admin
        admin = Administrator("admin", "admin@airline.com", "admin1234", "+1234567890", 
                              "ADMIN001", "System Admin")
        cursor.execute("""
        INSERT INTO Administrator (username, email, password, contact_number, admin_id, role)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            admin.username, admin.email, admin.password, admin.contact_number,
            admin.admin_id, admin.role
        ))
        
        # Add sample crew member
        crew = CrewMember("crew", "crew@airline.com", "crew1234", "+9876543210", 
                          "CREW001", "Flight Attendant", "British Airways")
        cursor.execute("""
        INSERT INTO CrewMember (username, email, password, contact_number, crew_id, position, airline)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            crew.username, crew.email, crew.password, crew.contact_number,
            crew.crew_id, crew.position, crew.airline
        ))
        
        conn.commit()
        print("✅ Sample data added successfully!")
    except sqlite3.Error as e:
        print(f"❌ Error adding sample data: {e}")
        conn.rollback()
    finally:
        conn.close()

# Run the application
if __name__ == "__main__":
    initialize_database()
    add_sample_data()
    main() 

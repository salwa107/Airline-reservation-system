# import sqlite3
# import uuid
# from datetime import datetime

# def generate_id(prefix=''):
#     """Generate a unique ID with optional prefix."""
#     unique_id = str(uuid.uuid4())[:8]
#     return f"{prefix}{unique_id}"

# def register_passenger(username, email, password, contact_number, age=None, 
#                       gender=None, passport_number=None, frequent_flyer_status=None):
#     """Register a new passenger in the database."""
#     connection = sqlite3.connect('project_data.db')
#     cursor = connection.cursor()
    
#     try:
#         # Check if username already exists
#         cursor.execute("SELECT user_name FROM Passenger WHERE user_name = ?", (username,))
#         if cursor.fetchone():
#             connection.close()
#             return False, "Username already exists"
        
#         # Generate passenger ID
#         passenger_id = generate_id('P')
        
#         # Insert passenger record
#         cursor.execute("""
#         INSERT INTO Passenger (user_name, email, password, contact_number, 
#                              passenger_id, age, gender, passport_number, frequent_flyer_status)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (username, email, password, contact_number, passenger_id, 
#               age, gender, passport_number, frequent_flyer_status))
        
#         connection.commit()
#         connection.close()
#         return True, "Passenger registered successfully"
    
#     except sqlite3.Error as e:
#         connection.rollback()
#         connection.close()
#         return False, f"Database error: {str(e)}"

# def add_flight(airline, source, destination, departure_time, arrival_time, available_seats):
#     """Add a new flight to the database."""
#     connection = sqlite3.connect('project_data.db')
#     cursor = connection.cursor()
    
#     try:
#         # Generate flight ID
#         flight_id = generate_id('FL')
        
#         # Check if airports exist
#         cursor.execute("SELECT airport_id FROM Airport WHERE airport_id = ?", (source,))
#         if not cursor.fetchone():
#             connection.close()
#             return False, "Source airport does not exist"
            
#         cursor.execute("SELECT airport_id FROM Airport WHERE airport_id = ?", (destination,))
#         if not cursor.fetchone():
#             connection.close()
#             return False, "Destination airport does not exist"
        
#         # Insert flight record
#         cursor.execute("""
#         INSERT INTO Flight (flight_id, airline, source, destination, 
#                           departure_time, arrival_time, available_seats)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (flight_id, airline, source, destination, 
#               departure_time, arrival_time, available_seats))
        
#         # Update airport available flights count
#         cursor.execute("""
#         UPDATE Airport SET available_flights = available_flights + 1
#         WHERE airport_id IN (?, ?)
#         """, (source, destination))
        
#         connection.commit()
#         connection.close()
#         return True, flight_id
    
#     except sqlite3.Error as e:
#         connection.rollback()
#         connection.close()
#         return False, f"Database error: {str(e)}"

# def search_flights(source=None, destination=None, date=None):
#     """Search flights based on criteria."""
#     connection = sqlite3.connect('project_data.db')
#     cursor = connection.cursor()
    
#     query = "SELECT f.flight_id, f.airline, a1.name as source_airport, a2.name as destination_airport, " \
#             "f.departure_time, f.arrival_time, f.available_seats " \
#             "FROM Flight f " \
#             "JOIN Airport a1 ON f.source = a1.airport_id " \
#             "JOIN Airport a2 ON f.destination = a2.airport_id " \
#             "WHERE 1=1 "
    
#     params = []
    
#     if source:
#         query += "AND f.source = ? "
#         params.append(source)
    
#     if destination:
#         query += "AND f.destination = ? "
#         params.append(destination)
    
#     if date:
#         query += "AND date(f.departure_time) = date(?) "
#         params.append(date)
    
#     try:
#         cursor.execute(query, params)
#         flights = cursor.fetchall()
#         connection.close()
        
#         # Convert to list of dictionaries for easier use
#         columns = ['flight_id', 'airline', 'source_airport', 'destination_airport', 
#                   'departure_time', 'arrival_time', 'available_seats']
#         result = []
#         for flight in flights:
#             flight_dict = {columns[i]: flight[i] for i in range(len(columns))}
#             result.append(flight_dict)
        
#         return True, result
    
#     except sqlite3.Error as e:
#         connection.close()
#         return False, f"Database error: {str(e)}"

# def book_flight(passenger_username, flight_id, seat_number=None, ticket_class="Economy"):
#     """Book a flight for a passenger."""
#     connection = sqlite3.connect('project_data.db')
#     cursor = connection.cursor()
    
#     try:
#         # Check if flight exists and has available seats
#         cursor.execute("SELECT available_seats FROM Flight WHERE flight_id = ?", (flight_id,))
#         flight = cursor.fetchone()
#         if not flight:
#             connection.close()
#             return False, "Flight not found"
        
#         available_seats = flight[0]
#         if available_seats <= 0:
#             connection.close()
#             return False, "No available seats on this flight"
        
#         # Check if passenger exists
#         cursor.execute("SELECT user_name FROM Passenger WHERE user_name = ?", (passenger_username,))
#         if not cursor.fetchone():
#             connection.close()
#             return False, "Passenger not found"
        
#         # Generate IDs
#         ticket_id = generate_id('TKT')
#         booking_id = generate_id('BKG')
        
#         # Base price calculation (simplified)
#         if ticket_class == "Economy":
#             price = 200.0
#         elif ticket_class == "Business":
#             price = 500.0
#         else:  # First class
#             price = 1000.0
        
#         # Insert ticket record
#         cursor.execute("""
#         INSERT INTO Ticket (ticket_id, passenger, flight_id, seat_number, ticket_class, price, status)
#         VALUES (?, ?, ?, ?, ?, ?, 'Active')
#         """, (ticket_id, passenger_username, flight_id, seat_number, ticket_class, price))
        
#         # Insert booking record
#         cursor.execute("""
#         INSERT INTO Booking (booking_id, passenger, flight_id, ticket_id, status)
#         VALUES (?, ?, ?, ?, 'Confirmed')
#         """, (booking_id, passenger_username, flight_id, ticket_id))
        
#         # Update flight available seats
#         cursor.execute("""
#         UPDATE Flight SET available_seats = available_seats - 1
#         WHERE flight_id = ?
#         """, (flight_id,))
        
#         # Add loyalty points if applicable
#         cursor.execute("""
#         SELECT loyalty_id FROM LoyaltyProgram WHERE passenger = ?
#         """, (passenger_username,))
        
#         loyalty = cursor.fetchone()
#         if loyalty:
#             # Add points based on class
#             points = 50 if ticket_class == "Economy" else (100 if ticket_class == "Business" else 150)
#             cursor.execute("""
#             UPDATE LoyaltyProgram SET points = points + ?
#             WHERE passenger = ?
#             """, (points, passenger_username))
        
#         connection.commit()
#         connection.close()
#         return True, {"booking_id": booking_id, "ticket_id": ticket_id}
    
#     except sqlite3.Error as e:
#         connection.rollback()
#         connection.close()
#         return False, f"Database error: {str(e)}"

# def get_passenger_bookings(passenger_username):
#     """Get all bookings for a passenger."""
#     connection = sqlite3.connect('project_data.db')
#     cursor = connection.cursor()
    
#     try:
#         query = """
#         SELECT b.booking_id, f.flight_id, f.airline, a1.name as source, a2.name as destination,
#                f.departure_time, f.arrival_time, t.ticket_class, t.seat_number, b.status
#         FROM Booking b
#         JOIN Flight f ON b.flight_id = f.flight_id
#         JOIN Ticket t ON b.ticket_id = t.ticket_id
#         JOIN Airport a1 ON f.source = a1.airport_id
#         JOIN Airport a2 ON f.destination = a2.airport_id
#         WHERE b.passenger = ?
#         ORDER BY f.departure_time
#         """
        
#         cursor.execute(query, (passenger_username,))
#         bookings = cursor.fetchall()
#         connection.close()
        
#         # Convert to list of dictionaries
#         columns = ['booking_id', 'flight_id', 'airline', 'source', 'destination', 
#                   'departure_time', 'arrival_time', 'ticket_class', 'seat_number', 'status']
#         result = []
#         for booking in bookings:
#             booking_dict = {columns[i]: booking[i] for i in range(len(columns))}
#             result.append(booking_dict)
        
#         return True, result
    
#     except sqlite3.Error as e:
#         connection.close()
#         return False, f"Database error: {str(e)}"

# def cancel_booking(booking_id):
#     """Cancel a booking."""
#     connection = sqlite3.connect('project_data.db')
#     cursor = connection.cursor()
    
#     try:
#         # Check if booking exists
#         cursor.execute("SELECT flight_id, ticket_id FROM Booking WHERE booking_id = ?", (booking_id,))
#         booking = cursor.fetchone()
#         if not booking:
#             connection.close()
#             return False, "Booking not found"
        
#         flight_id, ticket_id = booking
        
#         # Update booking status
#         cursor.execute("UPDATE Booking SET status = 'Cancelled' WHERE booking_id = ?", (booking_id,))
        
#         # Update ticket status
#         cursor.execute("UPDATE Ticket SET status = 'Cancelled' WHERE ticket_id = ?", (ticket_id,))
        
#         # Restore available seat
#         cursor.execute("UPDATE Flight SET available_seats = available_seats + 1 WHERE flight_id = ?", (flight_id,))
        
#         connection.commit()
#         connection.close()
#         return True, "Booking cancelled successfully"
    
#     except sqlite3.Error as e:
#         connection.rollback()
#         connection.close()
#         return False, f"Database error: {str(e)}"

# def process_payment(passenger_username, amount, payment_method, booking_id=None):
#     """Process a payment for a booking."""
#     connection = sqlite3.connect('project_data.db')
#     cursor = connection.cursor()
    
#     try:
#         # Generate payment ID
#         payment_id = generate_id('PAY')
        
#         # Insert payment record
#         cursor.execute("""
#         INSERT INTO Payment (payment_id, passenger, amount, payment_method, status)
#         VALUES (?, ?, ?, ?, 'Completed')
#         """, (payment_id, passenger_username, amount, payment_method))
        
#         connection.commit()
#         connection.close()
#         return True, payment_id
    
#     except sqlite3.Error as e:
#         connection.rollback()
#         connection.close()
#         return False, f"Database error: {str(e)}"

# def get_flight_details(flight_id):
#     """Get detailed information about a flight."""
#     connection = sqlite3.connect('project_data.db')
#     cursor = connection.cursor()
    
#     try:
#         query = """
#         SELECT f.flight_id, f.airline, a1.name as source_airport, a2.name as destination_airport,
#                f.departure_time, f.arrival_time, f.available_seats
#         FROM Flight f
#         JOIN Airport a1 ON f.source = a1.airport_id
#         JOIN Airport a2 ON f.destination = a2.airport_id
#         WHERE f.flight_id = ?
#         """
        
#         cursor.execute(query, (flight_id,))
#         flight = cursor.fetchone()
        
#         if not flight:
#             connection.close()
#             return False, "Flight not found"
        
#         columns = ['flight_id', 'airline', 'source_airport', 'destination_airport', 
#                   'departure_time', 'arrival_time', 'available_seats']
#         result = {columns[i]: flight[i] for i in range(len(columns))}
        
#         connection.close()
#         return True, result
    
#     except sqlite3.Error as e:
#         connection.close()
#         return False, f"Database error: {str(e)}"

# def assign_crew(flight_id, crew_username, role):
#     """Assign a crew member to a flight."""
#     connection = sqlite3.connect('project_data.db')
#     cursor = connection.cursor()
    
#     try:
#         # Check if flight exists
#         cursor.execute("SELECT flight_id FROM Flight WHERE flight_id = ?", (flight_id,))
#         if not cursor.fetchone():
#             connection.close()
#             return False, "Flight not found"
        
#         # Check if crew member exists
#         cursor.execute("SELECT user_name FROM CrewMember WHERE user_name = ?", (crew_username,))
#         if not cursor.fetchone():
#             connection.close()
#             return False, "Crew member not found"
        
#         # Generate assignment ID
#         assignment_id = generate_id('ASG')
        
#         # Insert crew assignment
#         cursor.execute("""
#         INSERT INTO CrewAssignment (assignment_id, flight_id, crew_member, role, status)
#         VALUES (?, ?, ?, ?, 'Assigned')
#         """, (assignment_id, flight_id, crew_username, role))
        
#         connection.commit()
#         connection.close()
#         return True, "Crew member assigned successfully"
    
#     except sqlite3.Error as e:
#         connection.rollback()
#         connection.close()
#         return False, f"Database error: {str(e)}"


    
#     except sqlite3.Error as e:
#         connection.rollback()
#         connection.close()
#         return False, f"Database error: {str(e)}"

# def add_airport(name, location):
#     """Add a new airport to the database."""
#     connection = sqlite3.connect('project_data.db')
#     cursor = connection.cursor()
    
#     try:
#         # Generate airport ID
#         airport_id = generate_id('APT')
        
#         # Insert airport record
#         cursor.execute("""
#         INSERT INTO Airport (airport_id, name, location, available_flights)
#         VALUES (?, ?, ?, 0)
#         """, (airport_id, name, location))
        
#         connection.commit()
#         connection.close()
#         return True, airport_id
    
#     except sqlite3.Error as e:
#         connection.rollback()
#         connection.close()
#         return False, f"Database error: {str(e)}"

# def add_airline(name, fleet_size, destinations, customer_rating):
#     """Add a new airline to the database."""
#     connection = sqlite3.connect('project_data.db')
#     cursor = connection.cursor()
    
#     try:
#         # Generate airline ID
#         airline_id = generate_id('AIR')
        
#         # Insert airline record
#         cursor.execute("""
#         INSERT INTO Airline (airline_id, name, fleet_size, destinations, customer_rating)
#         VALUES (?, ?, ?, ?, ?)
#         """, (airline_id, name, fleet_size, destinations, customer_rating))
        
#         connection.commit()
#         connection.close()
#         return True, airline_id
    
#     except sqlite3.Error as e:
#         connection.rollback()
#         connection.close()
#         return False, f"Database error: {str(e)}"
# ```

import sqlite3
def get_connection():
    return sqlite3.connect('project_data.db')
def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()
    
    # Passenger table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Passenger (
        user name TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        contact_number TEXT,
        passenger_id TEXT,
        age INTEGER,
        gender TEXT,
        passport_number TEXT,
        frequent_flyer_status TEXT
    )
    """)
    
    # Administrator table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Administrator (
        username TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        contact_number TEXT,
        admin_id TEXT UNIQUE,
        role TEXT
    )
    """)
    
    # CrewMember table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CrewMember (
        username TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        contact_number TEXT,
        crew_id TEXT UNIQUE,
        position TEXT,
        airline TEXT
    )
    """)
    
    # Airport table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Airport (
        airport_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        available_flights INTEGER DEFAULT 0
    )
    """)

    # Airline table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Airline (
        airline_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        fleet_size INTEGER,
        destinations TEXT,
        customer_rating REAL
    )
    """)

    # Flight table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Flight (
        flight_id TEXT PRIMARY KEY,
        airline TEXT NOT NULL,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        departure_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL,
        available_seats INTEGER NOT NULL,
        FOREIGN KEY (source) REFERENCES Airport(airport_id),
        FOREIGN KEY (destination) REFERENCES Airport(airport_id)
    )
    """)

    # Ticket table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ticket (
        ticket_id TEXT PRIMARY KEY,
        passenger TEXT NOT NULL,
        flight_id TEXT NOT NULL,
        seat_number TEXT,
        ticket_class TEXT NOT NULL,
        price REAL NOT NULL,
        status TEXT DEFAULT 'Active',
        FOREIGN KEY (passenger) REFERENCES Passenger(user_name),
        FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)
    )
    """)

    # Booking table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Booking (
        booking_id TEXT PRIMARY KEY,
        passenger TEXT NOT NULL,
        flight_id TEXT NOT NULL,
        ticket_id TEXT NOT NULL,
        status TEXT DEFAULT 'Confirmed',
        FOREIGN KEY (passenger) REFERENCES Passenger(user_name),
        FOREIGN KEY (flight_id) REFERENCES Flight(flight_id),
        FOREIGN KEY (ticket_id) REFERENCES Ticket(ticket_id)
    )
    """)

    # Payment table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Payment (
        payment_id TEXT PRIMARY KEY,
        passenger TEXT NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (passenger) REFERENCES Passenger(user_name)
    )
    """)

    # Baggage table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Baggage (
        baggage_id TEXT PRIMARY KEY,
        passenger TEXT NOT NULL,
        weight REAL NOT NULL,
        baggage_fee REAL DEFAULT 0.0,
        status TEXT DEFAULT 'Checked In',
        FOREIGN KEY (passenger) REFERENCES Passenger(user_name)
    )
    """)

    # Seat table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Seat (
        seat_id TEXT PRIMARY KEY,
        flight_id TEXT NOT NULL,
        seat_number TEXT NOT NULL,
        class_type TEXT NOT NULL,
        is_available BOOLEAN DEFAULT 1,
        FOREIGN KEY (flight_id) REFERENCES Flight(flight_id),
        UNIQUE(flight_id, seat_number)
    )
    """)

    # LoyaltyProgram table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS LoyaltyProgram (
        loyalty_id TEXT PRIMARY KEY,
        passenger TEXT UNIQUE NOT NULL,
        points INTEGER DEFAULT 0,
        membership_level TEXT DEFAULT 'Basic',
        FOREIGN KEY (passenger) REFERENCES Passenger(user_name)
    )
    """)

    # CrewAssignment table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CrewAssignment (
        assignment_id TEXT PRIMARY KEY,
        flight_id TEXT NOT NULL,
        crew_member TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT DEFAULT 'Assigned',
        FOREIGN KEY (flight_id) REFERENCES Flight(flight_id),
        FOREIGN KEY (crew_member) REFERENCES CrewMember(user_name)
    )
    """)

    # Create indexes for common queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_flight_source_dest ON Flight(source, destination)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_flight_departure ON Flight(departure_time)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_booking_passenger ON Booking(passenger)')
    
    connection.commit()
    connection.close()

def insert_sample_data():
    """Insert sample data for testing purposes."""
    connection = get_connection()
    cursor = connection.cursor()

    # Insert sample airports
    airports = [
        ('APT001', 'JFK International Airport', 'New York, USA', 0),
        ('APT002', 'LAX International Airport', 'Los Angeles, USA', 0),
        ('APT003', 'Heathrow Airport', 'London, UK', 0),
        ('APT004', 'Dubai International Airport', 'Dubai, UAE', 0),
        ('APT005', 'Tokyo Haneda Airport', 'Tokyo, Japan', 0)
    ]
    
    cursor.executemany("""
    INSERT OR IGNORE INTO Airport (airport_id, name, location, available_flights)
    VALUES (?, ?, ?, ?)
    """, airports)

    # Insert sample airlines
    airlines = [
        ('AIR001', 'Global Airways', 120, 'Global', 4.5),
        ('AIR002', 'TransContinental', 85, 'North America, Europe', 4.2),
        ('AIR003', 'Pacific Flyers', 65, 'Asia, Oceania', 4.3)
    ]
    
    cursor.executemany("""
    INSERT OR IGNORE INTO Airline (airline_id, name, fleet_size, destinations, customer_rating)
    VALUES (?, ?, ?, ?, ?)
    """, airlines)

    # Insert sample flights
    flights = [
        ('FL001', 'Global Airways', 'APT001', 'APT003', '2025-05-20 10:00:00', '2025-05-20 22:00:00', 150),
        ('FL002', 'TransContinental', 'APT002', 'APT004', '2025-05-21 12:00:00', '2025-05-22 02:00:00', 180),
        ('FL003', 'Pacific Flyers', 'APT003', 'APT005', '2025-05-22 14:00:00', '2025-05-23 04:00:00', 200)
    ]
    
    cursor.executemany("""
    INSERT OR IGNORE INTO Flight (flight_id, airline, source, destination, departure_time, arrival_time, available_seats)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, flights)

    # Insert a sample administrator account
    admin = ('admin', 'admin@airline.com', 'admin1234', '123-456-7890', 'ADM001', 'System Administrator')
    
    cursor.execute("""
    INSERT OR IGNORE INTO Administrator (user_name, email, password, contact_number, admin_id, role)
    VALUES (?, ?, ?, ?, ?, ?)
    """, admin)

    # Update available_flights count for airports
    cursor.execute("""
    UPDATE Airport 
    SET available_flights = (
        SELECT COUNT(*) FROM Flight WHERE source = Airport.airport_id OR destination = Airport.airport_id
    )
    """)

    connection.commit()
    connection.close()
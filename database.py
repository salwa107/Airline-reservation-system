import sqlite3

# Connect to SQLite database
connection = sqlite3.connect('project_data.db')
cursor = connection.cursor()

# Create the Passenger table (if it doesn't exist already)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Passenger (
    user_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    contact_number TEXT,  
    passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    gender TEXT,
    passport_number TEXT,  
    frequent_flyer_status TEXT
)
""")



connection.commit()  # Save changes
connection.close()  # Close the connection

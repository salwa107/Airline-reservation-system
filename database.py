
import sqlite3

def get_connection():
    return sqlite3.connect('project_data.db')

def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Passenger (
        user_name TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        password_hash BLOB  NOT NULL,
        contact_number TEXT,
        passenger_id TEXT,
        age INTEGER,
        gender TEXT,
        passport_number TEXT,
        frequent_flyer_status TEXT
    )
    """)
    
    connection.commit()
    connection.close()

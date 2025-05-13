# database.py
import sqlite3

def get_connection():
    return sqlite3.connect('project_data.db')

def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()
    
    # Passenger table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Passenger (
        user_name TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        password_hash BLOB NOT NULL,
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
        user_name TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        password_hash BLOB NOT NULL,
        contact_number TEXT,
        admin_id TEXT UNIQUE,
        role TEXT
    )
    """)
    
    # CrewMember table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CrewMember (
        user_name TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        password_hash BLOB NOT NULL,
        contact_number TEXT,
        crew_id TEXT UNIQUE,
        position TEXT,
        airline TEXT
    )
    """)
    
    connection.commit()
    connection.close()
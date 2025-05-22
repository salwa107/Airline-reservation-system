import unittest
import sqlite3
from OurPROJECT import *

class TestAirlineSystem(unittest.TestCase):

    def setUp(self):
        # Initialize fresh test database
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        
        # Create tables
        initialize_database()
        
        # Add a test flight
        self.cursor.execute("""
            INSERT INTO Flight VALUES 
            ('FL123', 'Test Air', 'JFK', 'LAX', '2025-01-01 08:00', 
             '2025-01-01 11:00', 150, 150, 200.00)
        """)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_passenger_signup(self):
        passenger = Passenger("testuser", "test@email.com", "pass123", "5551234567")
        result = passenger.sign_up(self.cursor, self.conn)
        self.assertTrue(result)
        self.assertEqual(passenger.username, "testuser")

    def test_duplicate_passenger_signup(self):
        passenger1 = Passenger("user1", "user1@test.com", "pass123", "1111111111")
        passenger1.sign_up(self.cursor, self.conn)
        
        passenger2 = Passenger("user1", "user2@test.com", "pass456", "2222222222")
        result = passenger2.sign_up(self.cursor, self.conn)
        self.assertFalse(result)

    def test_flight_booking(self):
        passenger = Passenger("flyer", "flyer@test.com", "pass123", "5551234567")
        passenger.sign_up(self.cursor, self.conn)
        
        result = passenger.book_flight("FL123", self.cursor, self.conn)
        self.assertTrue(result)
        
        # Verify booking exists
        self.cursor.execute("SELECT * FROM Booking WHERE passenger = ?", ("flyer",))
        booking = self.cursor.fetchone()
        self.assertIsNotNone(booking)

    def test_booking_cancellation(self):
        passenger = Passenger("flyer", "flyer@test.com", "pass123", "5551234567")
        passenger.sign_up(self.cursor, self.conn)
        passenger.book_flight("FL123", self.cursor, self.conn)
        
        # Get booking ID
        self.cursor.execute("SELECT booking_id FROM Booking WHERE passenger = ?", ("flyer",))
        booking_id = self.cursor.fetchone()[0]
        
        result = passenger.cancel_booking(booking_id, self.cursor, self.conn)
        self.assertTrue(result)
        
        # Verify booking removed
        self.cursor.execute("SELECT * FROM Booking WHERE booking_id = ?", (booking_id,))
        booking = self.cursor.fetchone()
        self.assertIsNone(booking)

    def test_view_bookings(self):
        passenger = Passenger("flyer", "flyer@test.com", "pass123", "5551234567")
        passenger.sign_up(self.cursor, self.conn)
        passenger.book_flight("FL123", self.cursor, self.conn)
        
        # This will print output, but we can verify no errors
        try:
            passenger.view_booking_details()
            result = True
        except:
            result = False
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()

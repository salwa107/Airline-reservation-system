import unittest
import ourproject

class TestReservationSystem(unittest.TestCase):

    def setUp(self):
        ourproject.reservations.clear()

    def test_booking_new_user(self):
        result = ourproject.book("Alice")
        self.assertEqual(result, "Booking confirmed for Alice")
        self.assertIn("Alice", ourproject.reservations)

    def test_booking_duplicate_user(self):
        ourproject.book("Bob")
        result = ourproject.book("Bob")
        self.assertEqual(result, "Bob already booked")

    def test_cancel_existing_user(self):
        ourproject.book("Charlie")
        result = ourproject.cancel("Charlie")
        self.assertEqual(result, "Booking cancelled for Charlie")
        self.assertNotIn("Charlie", ourproject.reservations)

    def test_cancel_nonexistent_user(self):
        result = ourproject.cancel("Diana")
        self.assertEqual(result, "Diana not found")

    def test_list_all(self):
        ourproject.book("Eve")
        ourproject.book("Frank")
        self.assertEqual(ourproject.list_reservations(), ["Eve", "Frank"])

if __name__ == '__main__':
    unittest.main()

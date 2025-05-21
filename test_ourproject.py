import unittest
import OurPROJECT

class TestReservationSystem(unittest.TestCase):

    def setUp(self):
        OurPROJECT.reservations.clear()

    def test_booking_new_user(self):
        result = OurPROJECT.book("Alice")
        self.assertEqual(result, "Booking confirmed for Alice")
        self.assertIn("Alice", OurPROJECT.reservations)

    def test_booking_duplicate_user(self):
        OurPROJECT.book("Bob")
        result = OurPROJECT.book("Bob")
        self.assertEqual(result, "Bob already booked")

    def test_cancel_existing_user(self):
        OurPROJECT.book("Charlie")
        result = OurPROJECT.cancel("Charlie")
        self.assertEqual(result, "Booking cancelled for Charlie")
        self.assertNotIn("Charlie", OurPROJECT.reservations)

    def test_cancel_nonexistent_user(self):
        result = OurPROJECT.cancel("Diana")
        self.assertEqual(result, "Diana not found")

    def test_list_all(self):
        OurPROJECT.book("Eve")
        OurPROJECT.book("Frank")
        self.assertEqual(OurPROJECT.list_reservations(), ["Eve", "Frank"])

if __name__ == '__main__':
    unittest.main()

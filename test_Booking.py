import unittest   # Importing Python's Built-in Unit Testing Framework
import sqlite3   # Import modules for manipulating SQLite databases
import os   # Import OS file path module

# Import the function to be tested from the main system module
from booking_system import generate_booking_id, is_valid_seat_format, is_seat_reserved, initial_database

# Create test classes
class TestBookingSystem(unittest.TestCase):

    def setUp(self):
        """Create a fresh test database before each test."""
        self.test_db = "test_airlines.db"   # Define the name of the database file for testing
        if os.path.exists(self.test_db):   # If a file with the same name previously existed
            os.remove(self.test_db)   # Delete the old database file
        initial_database(self.test_db)   # Initialise the system structure using the test database

    def tearDown(self):
        """Remove the test database after each test."""
        if os.path.exists(self.test_db):   # Clean up the test database after testing
            os.remove(self.test_db)   

    def test_generate_booking_id(self):
        booking_id = generate_booking_id()   # Calling a function to generate a predefined number
        self.assertEqual(len(booking_id), 8)   # Check that the length of the booking number is 8
        self.assertTrue(booking_id.isalnum())   # Check that the booking number is a combination of letters + numbers
        self.assertTrue(booking_id.isupper())   # Check that the booking number is a combination of letters + numbers

    def test_valid_seat_format(self):
        self.assertTrue(is_valid_seat_format("1A"))   # Code compliance
        self.assertTrue(is_valid_seat_format("5A"))   # Code compliance
        self.assertFalse(is_valid_seat_format("16A"))   # Out of scope (non-compliance)
        self.assertFalse(is_valid_seat_format("A1"))   # Wrong order (non-compliance)
        self.assertFalse(is_valid_seat_format("1B"))   # Non-A Seat (non-compliant)

    def test_is_seat_reserved(self):
        seat = "6A"   # Reserve a seat for testing
        self.assertFalse(is_seat_reserved(seat, self.test_db))   # Initial should not be booked
        
        # Insert a scheduled record for testing
        conn = sqlite3.connect(self.test_db)   # Linking test databases
        cursor = conn.cursor()   # Get cursor
        cursor.execute("INSERT INTO bookings (id, name, passport, seat, meal) VALUES (?, ?, ?, ?, ?)",
                       ("TST12345", "Alice", "P12345678", seat, "Vegetarian"))   # Insert test data

        conn.commit()   # Submit changes
        conn.close()   # close the connection

        self.assertTrue(is_seat_reserved(seat, self.test_db))   #  This should be booked

# Main programme entry: running test cases
if __name__ == '__main__':
    unittest.main()   # Start unit tests

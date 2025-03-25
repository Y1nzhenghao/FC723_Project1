# Apache Airlines - Final Version
# Version: Final
# Description: Adds a new function (meal preference selection)

import sqlite3 # Import SQLite Database Module
import random # Import the Generate Random Numbers module
import string # Import the string processing module

# ----------- database initialization -----------
def initial_database(db_name="airlines.db"):
    """
    Initialise the database: create the bookings table to store passenger booking information.
    If the database or table does not exist, it will be created automatically.
    """
    # Create the bookings table to store booking information.
    conn = sqlite3.connect(db_name)   # Connect to (or create) the SQLite database file
    cursor = conn.cursor()   # Create a cursor object to execute SQL commands
    
    # Execute SQL to create the 'bookings' table with fields for id, name, passport, seat, and meal preference
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS bookings(
                       id TEXT PRIMARY KEY,
                       name TEXT NOT NULL,
                       passport TEXT NOT NULL,
                       seat TEXT NOT  NULL,
                       meal TEXT
                       )
                   ''')
    conn.commit()   # Save changes.
    conn.close()   # Close the database connection.

# ----------- Tool Functions -----------
def generate_booking_id():
    """
    Generates an 8-digit random booking number consisting of uppercase letters and numbers.
    Used to uniquely identify each booking record.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))   # Return random ID.

def is_seat_reserved(seat,db_name="airlines.db"):
    """
    Checks if the specified seat has been booked.
    Returns True for booked, False for unavailable.
    """ 
    conn = sqlite3.connect(db_name)   # Connect to the database.
    cursor = conn.cursor()   # Create cursor.
    cursor.execute("SELECT * FROM bookings WHERE seat = ?", (seat.upper(),))   # Search for seat.
    result = cursor.fetchone()   # Fetch result
    conn.close()   # Close connection.
    return result is not None   # Return True if result exists

def is_valid_seat_format(seat):
    """
    Checks whether the seat format is valid.
    only allows 1A to 10A.
    """
    valid_seats = [f"{i}A" for i in range(1, 11)]   # Create list: ['1A',...,'10A'].
    return seat in valid_seats   # Return True if seat is in the valid list.

def view_seats():
    """
    Displays the booking status of the first 10 seats (1A to 10A).
    Use ‘R’ for booked and ‘F’ for free.
    """
    print("\n=== Seat status (1A - 10A) ===")   # Display heading.
    for row in range(1, 11):   # loop through the number 1 to 10.
        seat = f"{row}A"   # Create seat number string.
        status = "R" if is_seat_reserved(seat) else "F"   # Check status.
        print(f"Seat {seat}: {'Booked' if status == 'R' else 'Free'}")   # Print result.


def reserve_seat():
    """
    The user enters his name, passport number and seat number to make a booking.
    If the seat is available, a reservation number is generated and the information is saved to the database.
    Basic exception handling is included.
    """
    try:
        name = input("Please enter your name: ").strip()   # Get name input.
        passport = input("Please enter your passport number: ").strip()   # Get passport.
        seat = input("Please enter the seat number: ").strip().upper()   # Get seat number and convert to uppercase.
        
        # Validate seat format (must be between 1A and 10A)
        if not is_valid_seat_format(seat):
            print("Invalid seat number. Please enter a seat between 1A and 10A.")
            return

        # Display meal preference options to user.
        print("Meal Preferences: ")
        print("1. Standard")
        print("2. Vegetarian")
        print("3. Halal")
        print("4. No Meal")
        meal_choice = input("Select your meal preference (1-4): ").strip()   # Get choice.
        meal_map = {'1':'Standard','2':'Vegetarian','3':'Halal','4':'No Meal'}   # Map input to meal type.
        meal = meal_map.get(meal_choice,'Standard') # default to 'Standard' if invalid input
        
        
        # Check that the inputs are correct
        if not name or not passport or not seat:
            print('Input cannot be empty.')
            return
        
        # Determine if a seat is booked
        if is_seat_reserved(seat):
            print("This seat is already booked, please select another seat.")
            return

        # Generate booking number and import into database
        booking_id = generate_booking_id()   # Generate unique booking ID.

        conn = sqlite3.connect("airlines.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (id, name, passport, seat, meal) VALUES (?, ?, ?, ?, ?)",
                       (booking_id, name, passport, seat, meal))
        conn.commit()   # Save changes
        conn.close()   # Close changes
        
        # Display information
        print(f"The booking was successful! Your booking number is: {booking_id}")
        print(f"Meal preference: {meal}")
        
    except Exception as e:
        # Print any information that may be incorrect
        print("Booking Failure:",e)   
        
# Booking cancellation
def cancel_booking():
    """
    The user enters the reservation number to cancel the reservation.
    If the corresponding record is found, it is deleted from the database.
    """
    try:
        booking_id = input("Please enter the booking number to cancel the booking: ").strip().upper()   # Get input
        if not booking_id:
            print("Booking number cannot be empty. Please try again.")
            return
    
        conn = sqlite3.connect("airlines.db")   # Connect to database
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))   # Attempt deletion.
        conn.commit()   # Save changes
        if cursor.rowcount > 0:
            print("Booking cancelled.")   # Success message
        else:
            print("The corresponding booking number was not found.")   # Not found
        conn.close()
    except Exception as e:
        print("Failed cancellation:",e)   # Print error
    

def show_booking_info():
    """
    Displays all current bookings, listing number, name, passport number and seat by row.
    """
    try:
        conn = sqlite3.connect("airlines.db")   # Connect to database.
        cursor = conn.cursor()   # Create cursor
        cursor.execute("SELECT * FROM bookings")   # Get all bookings
        rows = cursor.fetchall()   # Retrieve all results.
        if rows:
            print("\n=== Current Booking Information ===")   # Title
            for row in rows:
                print(f"number: {row[0]} | name: {row[1]} | passport: {row[2]} | seat: {row[3]} | meal: {row[4]}")   # Display data
        else:
            print("There are no bookings available at this time.")   # No results
        conn.close()
    except Exception as e:
        print("Unable to read booking information:",e)   # Print error if any

# ----------- Main Menu Functions -----------
def main_menu():
    """
    Displays the main menu and handles user input.
    Includes all function entries and exit mechanisms.
    """
    initial_database() # Initialise the database before the program starts
    # Main loop, displays menu until user selects exit
    while True:
        print("\n=== Apache Airlines Booking system ===")
        print("1. Check Seat Status")   
        print("2. Reserve your seat")
        print("3. Cancellation")
        print("4. Show booking information")
        print("5. Log out of the system")
        
        # Get user input
        choice = input("Please enter the operation number: ").strip()

        # Call the appropriate function based on the user's choice
        if choice == '1':
            view_seats()   # Show seat status
        elif choice == '2':
            reserve_seat()   # Start reservation
        elif choice == '3':
            cancel_booking()   # Cancel booking
        elif choice == '4':
            show_booking_info()   # Show all bookings
        elif choice == '5':
            print("Thank you for using the Apache Airlines booking system,bye!")
            break   # Exit the loop and terminate the programme
        else:
            print("Invalid entry, enter a number between 1 and 5.")   # Invalid input
            
# ----------- Main Programme Entry -----------
if __name__ == "__main__":
    main_menu()   # Start the program



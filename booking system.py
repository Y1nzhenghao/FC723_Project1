# Apache Airlines - Third Version
# Version: Third
# Description: Complete system with exception handling, clear prompts, formatted output, and optimized code

import sqlite3 # Import SQLite Database Module
import random # Import the Generate Random Numbers module
import string # Import the string processing module

# ----------- database initialization -----------
def initial_database():
    """
    Initialise the database: create the bookings table to store passenger booking information.
    If the database or table does not exist, it will be created automatically.
    """
    # Create the bookings table to store booking information.
    conn = sqlite3.connect("airlines.db")
    cursor = conn.cursor()
    
    # Create a table: bookings
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS bookings(
                       id TEXT PRIMARY KEY,
                       name TEXT NOT NULL,
                       passport TEXT NOT NULL,
                       seat TEXT NOT  NULL
                       )
                   ''')
    conn.commit()
    conn.close()

# ----------- Tool Functions -----------
def generate_booking_id():
    """
    Generates an 8-digit random booking number consisting of uppercase letters and numbers.
    Used to uniquely identify each booking record.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def is_seat_reserved(seat):
    """
    Checks if the specified seat has been booked.
    Returns True for booked, False for unavailable.
    """
    conn = sqlite3.connect("airlines.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE seat = ?", (seat.upper(),))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def view_seats():
    """
    Displays the booking status of the first 10 seats (1A to 10A).
    Use ‘R’ for booked and ‘F’ for free.
    """
    print("\n=== Seat status (1A - 10A) ===")
    for row in range(1, 11):
        seat = f"{row}A"
        status = "R" if is_seat_reserved(seat) else "F"
        print(f"Seat {seat}: {'Booked' if status == 'R' else 'Free'}")


def reserve_seat():
    """
    用户输入姓名、护照号和座位号来进行预订。
    如果座位可用，则生成预订编号并将信息保存至数据库。
    包含基本异常处理。
    """
    try:
        name = input("Please enter your name：").strip()
        passport = input("Please enter your passport number：").strip()
        seat = input("Please enter the seat number：").strip().upper()
        
        # Check that the inputs are correct
        if not name or not passport or not seat:
            print('Input cannot be empty.')
            return
        
        # Determine if a seat is booked
        if is_seat_reserved(seat):
            print("This seat is already booked, please select another seat.")
            return

        # Generate booking number and import into database
        booking_id = generate_booking_id()

        conn = sqlite3.connect("airlines.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (id, name, passport, seat) VALUES (?, ?, ?, ?)",
                       (booking_id, name, passport, seat))
        conn.commit()
        conn.close()    
        
        print(f"The booking was successful! Your booking number is：{booking_id}")
        
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
        booking_id = input("Please enter the booking number to cancel the booking：").strip().upper()
        if not booking_id:
            print("The booking number cannot be empty.")
            return
    
        conn = sqlite3.connect("airlines.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Booking cancelled。")
        else:
            print("The corresponding booking number was not found.")
        conn.close()
    except Exception as e:
        print("Failed cancellation:",e)
    

def show_booking_info():
    """
    Displays all current bookings, listing number, name, passport number and seat by row.
    """
    try:
        conn = sqlite3.connect("airlines.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        rows = cursor.fetchall()
        if rows:
            print("\n=== Current Booking Information ===")
            for row in rows:
                print(f"number: {row[0]} | name: {row[1]} | passport: {row[2]} | seat: {row[3]}")
        else:
            print("There are no bookings available at this time.")
        conn.close()
    except Exception as e:
        print("Unable to read booking information:",e)  

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
            view_seats()
        elif choice == '2':
            reserve_seat()
        elif choice == '3':
            cancel_booking()
        elif choice == '4':
            show_booking_info()
        elif choice == '5':
            print("Thank you for using the Apache Airlines booking system,bye!")
            break   # Exit the loop and terminate the programme
        else:
            print("Invalid entry, enter a number between 1 and 5.")
            
# ----------- Main Programme Entry -----------
if __name__ == "__main__":
    main_menu()



# Apache Airlines - Second Version
# Version: Function Implementation
# Description: Implements core features: seat viewing, reservation, cancellation, and booking info with database integration

import sqlite3
import random
import string

# ----------- database initialization -----------
def initial_database():
    # Connect to database file (create if it does not exist)
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

# Generate 8-digit random booking number (alpha + numeric)
def generate_booking_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Check if the seat is booked
def is_seat_reserved(seat):
    conn = sqlite3.connect("airlines.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE seat = ?", (seat,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# View seat status (Simple display of the status of some seats)
def view_seats():
    print("\n=== Seat status (partial example) ===")
    for row in range(1, 11):
        seat = f"{row}A"
        status = "R" if is_seat_reserved(seat) else "F"
        print(f"Seat {seat}: {status}")


# Seat reservations 
def reserve_seat():
    name = input("Please enter your name：")
    passport = input("Please enter your passport number：")
    seat = input("Please enter the seat number：")

    if is_seat_reserved(seat):
        print("This seat is already booked, please select another seat.")
        return

    booking_id = generate_booking_id()

    conn = sqlite3.connect("airlines.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (id, name, passport, seat) VALUES (?, ?, ?, ?)",
                   (booking_id, name, passport, seat))
    conn.commit()
    conn.close()
    
    print(f"The booking was successful! Your booking number is：{booking_id}")

# Booking cancellation
def cancel_booking():
    booking_id = input("Please enter the booking number to cancel the booking：")
    conn = sqlite3.connect("airlines.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Booking cancelled。")
    else:
        print("The corresponding booking number was not found.")
    conn.close()
    
# Display booking information
def show_booking_info():
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

# ----------- Main Menu Functions -----------
def main_menu():
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
        choice = input("Please enter the operation number: ")

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
            print("Thank you for using the Apache Airlines booking system!")
            break   # Exit the loop and terminate the programme
        else:
            print("Invalid input, please reselect.")
            
# ----------- Main Programme Entry -----------
if __name__ == "__main__":
    main_menu()



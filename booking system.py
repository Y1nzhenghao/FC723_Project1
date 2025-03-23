# Apache Airlines - Initial Version
# Version: Initial
# Description: Basic menu structure with placeholder functions

# View seat status (placeholder function)
def view_seats():
    print("[Function not yet implemented] View Seat Status")

# Seat reservations (placeholder function)
def reserve_seat():
    print("[Function not yet realised] Seat reservation")

# Booking cancellation (placeholder function)
def cancel_booking():
    print("[Function not yet implemented] Cancellation of booking")

# Display booking information (placeholder function)
def show_booking_info():
    print("[Function not yet implemented] Show booking information")

# ----------- Main Menu Functions -----------
def main_menu():
    # Main loop, displays menu until user selects exit
    while True:
        print("\n=== Apache Airlines Booking system ===")
        print("1. Check Seat Status")
        print("2. Reserve your seat")
        print("3. Cancellation")
        print("4. 显示预订信息")
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



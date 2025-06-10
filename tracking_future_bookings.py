import csv
from datetime import datetime

# Helper functions for managing bookings

# Function to save updated data back to the CSV file
def save_to_csv(file_path, data, fieldnames):
    """Save the updated data back to the CSV file."""
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Function to display booking details in a user-friendly format
def display_booking_info(booking):
    print("\nBooking Information:")
    print(f"Room ID: {booking.get('room_id', 'The room will be assigned by hotel reservation agents')}")
    print(f"First Name: {booking.get('first_name', 'N/A')}")
    print(f"Last Name: {booking.get('last_name', 'N/A')}")
    print(f"Phone Number: {booking.get('phone_number', 'N/A')}")
    print(f"Reserved From: {booking.get('reserved_from', 'N/A')}")
    print(f"Reserved To: {booking.get('reserved_to', 'N/A')}")
    print()

# Function to search for a guest by their first name
def search_upcoming_guest_by_name(bookings_data, first_name):
    results = [guest for guest in bookings_data if 'first_name' in guest and first_name.lower() in guest['first_name'].lower()]
    if len(results) > 1:
        print(f"Multiple guests found with the first name '{first_name}'. Please provide the last name.")
        last_name = input("Enter last name: ").strip().lower()
        results = [guest for guest in results if 'last_name' in guest and last_name == guest['last_name'].strip().lower()]
    if not results:
        print(f"No upcoming guests found with the name '{first_name}'.")
    return results

# Function to search for a guest by their last name
def search_upcoming_guest_by_last_name(bookings_data, last_name):
    results = [guest for guest in bookings_data if 'last_name' in guest and last_name.lower() in guest['last_name'].lower()]
    if len(results) > 1:
        print(f"Multiple guests found with the last name '{last_name}'. Please provide the first name.")
        first_name = input("Enter first name: ").strip().lower()
        results = [guest for guest in results if 'first_name' in guest and first_name == guest['first_name'].strip().lower()]
    if not results:
        print(f"No upcoming guests found with the last name '{last_name}'.")
    return results

# Function to search for bookings by check-in date
def search_upcoming_guests_by_checkin_date(bookings_data, check_in_date):
    results = [guest for guest in bookings_data if 'reserved_from' in guest and guest['reserved_from'] == check_in_date]
    if not results:
        print(f"No upcoming guests found for the check-in date '{check_in_date}'.")
    return results

# Function to add a new reservation to the bookings
def add_upcoming_reservation(bookings_data):
    new_reservation = {}
    new_reservation['first_name'] = input("Enter guest first name: ").strip()
    new_reservation['last_name'] = input("Enter guest last name: ").strip()
    new_reservation['phone_number'] = input("Enter guest contact information: ").strip()
    new_reservation['reserved_from'] = input("Enter check-in date (YYYY-MM-DD): ").strip()
    new_reservation['reserved_to'] = input("Enter check-out date (YYYY-MM-DD): ").strip()

    # Validate check-in and check-out dates
    checkin_date = new_reservation['reserved_from']
    checkout_date = new_reservation['reserved_to']
    today = datetime.now().date()
    checkin = datetime.strptime(checkin_date, "%Y-%m-%d").date()
    checkout = datetime.strptime(checkout_date, "%Y-%m-%d").date()

    if checkin <= today:
        print("Check-in date must be from tomorrow onwards.")
        return
    if checkout <= checkin:
        print("Check-out date must be after the check-in date.")
        return

    new_reservation['room_id'] = ""  # Room will be assigned by reservation agents prior to the guests' arrival

    bookings_data.append(new_reservation)
    save_to_csv('Future booking.csv', bookings_data, bookings_data[0].keys())

    print("\nReservation was made successfully with the following details:")
    display_booking_info(new_reservation)

# Function to modify check-in or check-out dates for an existing booking
def modify_booking_dates(bookings_data):
    first_name = input("Enter guest first name: ").strip().lower()
    last_name = input("Enter guest last name: ").strip().lower()

    results = [guest for guest in bookings_data if 
               guest.get('first_name', '').lower() == first_name and 
               guest.get('last_name', '').lower() == last_name]

    if not results:
        print(f"No booking found for {first_name.title()} {last_name.title()}.")
        return

    booking_to_modify = results[0]
    print("\nBooking to be modified:")
    display_booking_info(booking_to_modify)

    new_checkin = input("Enter new check-in date (YYYY-MM-DD): ").strip()
    new_checkout = input("Enter new check-out date (YYYY-MM-DD): ").strip()

    today = datetime.now().date()
    checkin = datetime.strptime(new_checkin, "%Y-%m-%d").date()
    checkout = datetime.strptime(new_checkout, "%Y-%m-%d").date()

    if checkin <= today:
        print("Check-in date must be from tomorrow onwards.")
        return
    if checkout <= checkin:
        print("Check-out date must be after the check-in date.")
        return

    booking_to_modify['reserved_from'] = new_checkin
    booking_to_modify['reserved_to'] = new_checkout

    save_to_csv('Future booking.csv', bookings_data, bookings_data[0].keys())

    print("\nBooking dates updated successfully. Here are the updated details:")
    display_booking_info(booking_to_modify)

# Function to cancel an existing booking
def cancel_booking(bookings_data):
    first_name = input("Enter guest first name: ").strip().lower()
    last_name = input("Enter guest last name: ").strip().lower()

    results = [guest for guest in bookings_data if 
               guest.get('first_name', '').lower() == first_name and 
               guest.get('last_name', '').lower() == last_name]

    if not results:
        print(f"No booking found for {first_name.title()} {last_name.title()}.")
        return

    booking_to_cancel = results[0]
    print("\nBooking to be canceled:")
    display_booking_info(booking_to_cancel)

    confirm = input("Are you sure you want to cancel this booking? (yes/no): ").strip().lower()
    if confirm in ['yes', 'y']:
        bookings_data.remove(booking_to_cancel)
        save_to_csv('Future booking.csv', bookings_data, bookings_data[0].keys())
        print("\nThe booking has been successfully canceled.")
    else:
        print("\nThe booking was not canceled.")

# Main function to manage all booking-related operations
def track_bookings_operations(bookings_data):
    while True:
        print("\nTrack Bookings Operations:")
        print("1. Search upcoming guest by name")
        print("2. Search upcoming guest by last name")
        print("3. Search upcoming guests by check-in date")
        print("4. Add upcoming reservation")
        print("5. Modify booking dates")
        print("6. Cancel a booking")
        print("7. Go back")

        choice = input("Choose an operation: ")

        if choice == "1":
            first_name = input("Enter guest first name: ").strip()
            results = search_upcoming_guest_by_name(bookings_data, first_name)
            for guest in results:
                display_booking_info(guest)

        elif choice == "2":
            last_name = input("Enter guest last name: ").strip()
            results = search_upcoming_guest_by_last_name(bookings_data, last_name)
            for guest in results:
                display_booking_info(guest)

        elif choice == "3":
            check_in_date = input("Enter check-in date (YYYY-MM-DD): ").strip()
            results = search_upcoming_guests_by_checkin_date(bookings_data, check_in_date)
            for guest in results:
                display_booking_info(guest)

        elif choice == "4":
            add_upcoming_reservation(bookings_data)

        elif choice == "5":
            modify_booking_dates(bookings_data)

        elif choice == "6":
            cancel_booking(bookings_data)

        elif choice == "7":
            break

        else:
            print("Invalid choice. Please try again.")

import csv
from datetime import datetime, timedelta
from company_operations import company_operations
from tracking_future_bookings import track_bookings_operations
from service_operations import services_operations

# Load datasets
def load_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_to_csv(file_path, data, fieldnames):
    """Save the updated data back to the CSV file."""
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

guest_data = load_csv('Guest.csv')
company_data = load_csv('Companies.csv')
booking_data = load_csv('Future booking.csv')
services_data = load_csv('Hotel_Services.csv')

def search_guest_by_name(name):
    try:
        results = [guest for guest in guest_data if 'first_name' in guest and name.lower() in guest['first_name'].lower()]
        if len(results) > 1:
            print(f"Multiple guests found with the name '{name}'. Please provide the last name.")
            last_name = input("Enter last name: ").strip().lower()
            results = [guest for guest in results if 'last_name' in guest and last_name == guest['last_name'].strip().lower()]
        if not results:
            print(f"No match found for the name '{name}'. Check the available names in the dataset.")
        return results
    except KeyError:
        print("Error: 'first_name' or 'last_name' column not found in the dataset. Available keys are:", guest_data[0].keys())
        return []

def search_guest_by_id(guest_id):
    try:
        results = [guest for guest in guest_data if 'guest_id' in guest and guest['guest_id'] == guest_id]
        if not results:
            print(f"No match found for guest ID '{guest_id}'.")
        return results
    except KeyError:
        print("Error: 'guest_id' column not found in the dataset. Available keys are:", guest_data[0].keys())
        return []

def search_guests_by_checkin_date(checkin_date):
    try:
        results = [guest for guest in guest_data if 'check_in_date' in guest and guest['check_in_date'] == checkin_date]
        if not results:
            print(f"No guests found for the check-in date '{checkin_date}'.")
        return results
    except KeyError:
        print("Error: 'check_in_date' column not found in the dataset. Available keys are:", guest_data[0].keys())
        return []

def display_guest_info(guest):
    print("\nGuest Information:")
    for key, value in guest.items():
        print(f"{key}: {value}")
    print()

def modify_guest_data(guest_id, updates):
    for guest in guest_data:
        if 'guest_id' in guest and guest['guest_id'] == guest_id:
            for field, new_value in updates.items():
                if field in guest:
                    guest[field] = new_value
                else:
                    print(f"Error: Field '{field}' not found in the dataset.")
                    return False
            save_to_csv('Guest.csv', guest_data, guest.keys())
            return True
    print("Guest ID not found.")
    return False

def ask_to_go_back():
    while True:
        choice = input("Do you want to go back to the main menu? (yes/no): ").strip().lower()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            exit_choice = input("Do you want to exit the program? (yes/no): ").strip().lower()
            if exit_choice in ['yes', 'y']:
                print("Thank you for using Python Hotel System!")
                exit()
            elif exit_choice in ['no', 'n']:
                return False
            else:
                print("Invalid input. Please type 'yes' or 'no'.")
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

def validate_dates(checkin_date, checkout_date):
    today = datetime.now().date()
    checkin = datetime.strptime(checkin_date, "%Y-%m-%d").date()
    checkout = datetime.strptime(checkout_date, "%Y-%m-%d").date()

    if checkin <= today:
        print("Check-in date must be from tomorrow onwards.")
        return False
    if checkout <= checkin:
        print("Check-out date must be after the check-in date.")
        return False
    return True

def guest_operations():
    while True:
        print("\nGuest Operations:")
        print("1. Search guest by name")
        print("2. Search guest by ID")
        print("3. Search guests by check-in date")
        print("4. Change check-out date")
        print("5. Go back")

        choice = input("Choose an operation: ")

        if choice == "1":
            name = input("Enter guest name to search: ")
            results = search_guest_by_name(name)
            if results:
                for guest in results:
                    display_guest_info(guest)
            else:
                print("No guests found.")

        elif choice == "2":
            guest_id = input("Enter guest ID to search: ")
            results = search_guest_by_id(guest_id)
            if results:
                for guest in results:
                    display_guest_info(guest)
            else:
                print("No guest found with this ID.")

        elif choice == "3":
            checkin_date = input("Enter check-in date (YYYY-MM-DD): ")
            results = search_guests_by_checkin_date(checkin_date)
            if results:
                for guest in results:
                    display_guest_info(guest)
            else:
                print("No guests found for this date.")

        elif choice == "4":
            guest_id = input("Enter guest ID to modify: ")
            new_checkout = input("Enter new check-out date (YYYY-MM-DD): ")
            checkin_date = next((guest['check_in_date'] for guest in guest_data if guest['guest_id'] == guest_id), None)
            if checkin_date and validate_dates(checkin_date, new_checkout):
                success = modify_guest_data(guest_id, {'check_out_date': new_checkout})
            else:
                success = False

            if success:
                print("Modification successful.")
            else:
                print("Guest ID not found or field is incorrect.")

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")

def main():
    while True:
        print("\nWELCOME TO PYTHON HOTEL SYSTEM")
        print("Hotel Management System:")
        print("1. Work with Guest Information")
        print("2. Work with Company Information")
        print("3. Track Bookings")
        print("4. Manage Services")
        print("5. Exit")

        main_choice = input("Choose an option: ")

        if main_choice == "1":
            guest_operations()
        elif main_choice == "2":
            company_operations(company_data)
        elif main_choice == "3":
            track_bookings_operations(booking_data)
        elif main_choice == "4":
            services_operations(services_data)
        elif main_choice == "5":
            print("Thank you for using Python Hotel System!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

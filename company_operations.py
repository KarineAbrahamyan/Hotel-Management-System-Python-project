import csv

# Helper functions for companies

# Function to save updated data back to the CSV file
def save_to_csv(file_path, data, fieldnames):
    """Save the updated data back to the CSV file."""
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Function to display detailed company information
def display_company_info(company):
    print("\nCompany Information:")
    print(f"Company Name: {company.get('Company Name', 'N/A')}")
    print(f"Company Type: {company.get('Company Type', 'N/A')}")
    print(f"Nights Occupied Last Year: {company.get('Nights Occupied Last Year', 'N/A')}")
    print(f"Cooperation Status: {company.get('Cooperation Status', 'N/A')}")
    print(f"Standard Price: {company.get('Standard Price', 'N/A')}")
    print(f"Twin Price: {company.get('Twin Price', 'N/A')}")
    print(f"Accessible Price: {company.get('Accessible Price', 'N/A')}")
    print(f"Deluxe Price: {company.get('Deluxe Price', 'N/A')}")
    print(f"Family Deluxe Price: {company.get('Family Deluxe Price', 'N/A')}")
    print(f"Suite Price: {company.get('Suite Price', 'N/A')}")

# Function to search for a company by name
def search_company_by_name(company_data, name):
    try:
        # Filter companies matching the name
        results = [company for company in company_data if 'Company Name' in company and name.lower() in company['Company Name'].lower()]
        if results:
            # Display information for all matching companies
            for company in results:
                display_company_info(company)
        else:
            print(f"No match found for the company name '{name}'.")
    except KeyError:
        print("Error: 'Company Name' column not found in the dataset. Available keys are:", company_data[0].keys())

# Function to search for companies by type
def search_company_by_type(company_data):
    try:
        # Extract unique company types
        types = {company['Company Type'] for company in company_data}
        print("Available Company Types:")
        for idx, company_type in enumerate(types, start=1):
            print(f"{idx}. {company_type}")

        # Prompt user to select a company type
        choice = input("Select a company type by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(types):
            selected_type = list(types)[int(choice) - 1]
            results = [company for company in company_data if company['Company Type'] == selected_type]
            print(f"Companies of type '{selected_type}':")
            for company in results:
                display_company_info(company)
        else:
            print("Invalid choice.")
    except KeyError:
        print("Error: 'Company Type' column not found in the dataset. Available keys are:", company_data[0].keys())

# Function to calculate discounted prices based on nights occupied
def calculate_discounted_prices(company_data):
    try:
        # Prompt user to enter company name
        company_name = input("Enter the company name: ")
        company = next((c for c in company_data if c['Company Name'].lower() == company_name.lower()), None)
        if not company:
            print(f"No company found with the name '{company_name}'.")
            return

        # Determine discount based on nights occupied
        nights_occupied = int(company['Nights Occupied Last Year'])
        if nights_occupied < 50:
            discount = 0.05
        elif 50 <= nights_occupied < 100:
            discount = 0.10
        elif 100 <= nights_occupied < 150:
            discount = 0.12
        else:
            discount = 0.15

        print(f"The company '{company_name}' has occupied {nights_occupied} nights within a year and gets a {int(discount * 100)}% discount.")
        # Calculate and display discounted prices for each room type
        for room_type in ['Standard Price', 'Twin Price', 'Accessible Price', 'Deluxe Price', 'Family Deluxe Price', 'Suite Price']:
            original_price = int(float(company[room_type]))
            discounted_price = int(original_price * (1 - discount))
            print(f"{room_type}: Original Price: {original_price}, Discounted Price: {discounted_price}")
    except KeyError as e:
        print(f"Error: Missing required column '{e.args[0]}' in the dataset.")
    except ValueError:
        print("Error: Invalid numeric value in the dataset.")

# Function to change the cooperation status of a company
def change_cooperation_status(company_data):
    try:
        # Prompt user to enter company name
        company_name = input("Enter the company name: ")
        company = next((c for c in company_data if c['Company Name'].lower() == company_name.lower()), None)
        if not company:
            print(f"No company found with the name '{company_name}'.")
            return

        # Display current status and available statuses to change
        current_status = company['Cooperation Status']
        print(f"Current Cooperation Status: {current_status}")
        available_statuses = ['Active', 'Inactive', 'Pending']
        available_statuses.remove(current_status)
        print("Available statuses to change:")
        for idx, status in enumerate(available_statuses, start=1):
            print(f"{idx}. {status}")

        # Prompt user to select a new status
        choice = input("Select the new status by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(available_statuses):
            new_status = available_statuses[int(choice) - 1]
            company['Cooperation Status'] = new_status
            save_to_csv('Companies.csv', company_data, company_data[0].keys())
            print(f"Cooperation status changed to '{new_status}'.")
        else:
            print("Invalid choice.")
    except KeyError as e:
        print(f"Error: Missing required column '{e.args[0]}' in the dataset.")

# Main function to manage all company-related operations
def company_operations(company_data):
    while True:
        # Display operation menu
        print("\nCompany Operations:")
        print("1. Search company by name")
        print("2. Search company by type")
        print("3. Calculate discounted corporate prices")
        print("4. Change cooperation status")
        print("5. Go back")

        # Get user choice
        choice = input("Choose an operation: ")

        if choice == "1":
            # Search company by name
            name = input("Enter company name to search: ")
            search_company_by_name(company_data, name)

        elif choice == "2":
            # Search companies by type
            search_company_by_type(company_data)

        elif choice == "3":
            # Calculate discounted prices
            calculate_discounted_prices(company_data)

        elif choice == "4":
            # Change cooperation status
            change_cooperation_status(company_data)

        elif choice == "5":
            # Exit the company operations menu
            break

        else:
            # Handle invalid input
            print("Invalid choice. Please try again.")
import csv

# Helper functions for managing hotel services

# Function to display a list of all hotel services
def display_service_list(services_data):
    print("\nList of Hotel Services:")
    # Iterate through each service in the list and display its name
    for service in services_data:
        print(f"- {service.get('Service Name', 'N/A')}")
    print()

# Function to display detailed information about a specific service
def display_service_info(service):
    print("\nService Information:")
    # Loop through the key-value pairs in the service dictionary and display them
    for key, value in service.items():
        print(f"{key}: {value}")
    print()

# Function to allow the user to select and view details of a specific service
def get_service_by_number(services_data):
    print("\nAvailable Services:")
    # Display a numbered list of services for user selection
    for idx, service in enumerate(services_data, start=1):
        print(f"{idx}. {service.get('Service Name', 'N/A')}")

    # Prompt the user to select a service by its number
    choice = input("Choose a service by number: ").strip()
    
    # Check if the input is valid (a number within the range of available services)
    if choice.isdigit() and 1 <= int(choice) <= len(services_data):
        # Retrieve the selected service based on the user's input
        selected_service = services_data[int(choice) - 1]
        # Display detailed information about the selected service
        display_service_info(selected_service)
    else:
        # Display an error message for invalid input
        print("Invalid choice. Please try again.")

# Main function to handle hotel services operations
def services_operations(services_data):
    while True:
        # Display the main menu for service operations
        print("\nHotel Services Operations:")
        print("1. See the list of hotel services")
        print("2. Get specific service information")
        print("3. Go back")

        # Prompt the user to choose an operation
        choice = input("Choose an operation: ").strip()

        # Option 1: Display the list of all hotel services
        if choice == "1":
            display_service_list(services_data)

        # Option 2: Allow the user to view details of a specific service
        elif choice == "2":
            get_service_by_number(services_data)

        # Option 3: Exit the loop and return to the previous menu
        elif choice == "3":
            break

        # Handle invalid input with an error message
        else:
            print("Invalid choice. Please try again.")
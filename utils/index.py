import csv
import os
from datetime import datetime

def read_reference_number(file_path):
    if not os.path.exists(file_path):
        return 10
    with open(file_path, 'r') as file:
        return int(file.read().strip())

def write_reference_number(file_path, ref_number):
    with open(file_path, 'w') as file:
        file.write(str(ref_number))

def get_customer_number(file_path, customer_email):
    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if present
        for row in reader:
            if len(row) >= 6 and row[5] == customer_email:  # Check if Email (column 5) matches
                return int(row[0])  # Return the Customer Number (column 0)

    return None

# Function to display existing customers
def display_customers(file_path, customer_type_filter=None):
    if not os.path.exists(file_path):
        print("No customers found.")
        return []

    customers = []
    display_index = 1  # Counter for displaying the prompt option

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header if present

        for i, row in enumerate(reader, start=1):
            # Ensure the row has enough columns
            while len(row) < 10:
                column_name = get_column_name(len(row))
                new_value = input(f"Enter value for {column_name}: ").strip()
                row.append(new_value)
                print(f"Updated row {i}: {row}")

            # Check customer type from the CSV and filter based on user input (0 or 1)
            row_customer_type = row[1].strip()  # Use the raw value since it's now numeric
            if (
                customer_type_filter is None or  # Show all customers if no filter is applied
                (customer_type_filter == row_customer_type) or  # Match the exact numeric type
                (row_customer_type == '')  # Include customers with unspecified type in both options
            ):
                customers.append(row)
                # Display 'Corporate' or 'Private' based on the numeric type
                display_type = 'Corporate' if row_customer_type == '1' else 'Private' if row_customer_type == '0' else 'Unspecified'
                
                # Print with display index instead of i
                print(f"{display_index}: {display_type} - {row[4]} {row[2]} ({row[5]})")  # Display customer type, contact name, and email
                display_index += 1  # Increment the display counter

    if not customers:
        print("No customers found in the file.")
    return customers

def get_column_name(column_index):
    column_names = [
        "Customer Number", "Customer Type", "Company Name", "VAT Number",
        "Contact Name", "Email", "Street Address", "Postcode", "City", "Country"
    ]
    return column_names[column_index]

# Function to prompt user to select or create a customer
def select_or_create_customer(customers):
    selected_customer = None

    if customers:
        print("\nSelect a customer from the list above by entering the number or type 'N' to create a new customer:")
        selection = input().strip()

        if selection.lower() == 'n':
            print("Creating a new customer...")
        elif selection.isdigit() and 1 <= int(selection) <= len(customers):
            selected_customer = customers[int(selection) - 1]
        else:
            print("Invalid selection. Please try again.")
            exit(1)
    else:
        # No customers found, prompt user to press 'N' to create a new customer
        print("\nNo customers found. Press 'N' to create a new customer.")
        selection = input().strip()

        if selection.lower() == 'n':
            print("Creating a new customer...")
        else:
            print("Invalid selection. Please press 'N' to create a new customer.")
            exit(1)

    return selected_customer

def read_last_customer_number(file_path):
    if not os.path.exists(file_path):
        return 100001  # Start from 100001 if the file doesn't exist

    max_customer_number = 100001  # Initialize with the starting value

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader, None)  # Skip the header if present

        for row in reader:
            if len(row) > 0 and row[0].isdigit():  # Ensure the row has data and the first column is numeric
                customer_number = int(row[0])
                if customer_number > max_customer_number:
                    max_customer_number = customer_number

    return max_customer_number

def calculate_check_digit(reference):
    weights = [7, 3, 1]
    total = 0
    for i, digit in enumerate(reversed(reference)):
        total += int(digit) * weights[i % 3]
    return str((10 - (total % 10)) % 10)

def generate_finnish_reference_number(customer_number, base_number):
    customer_number_str = str(customer_number).zfill(6)  # Ensure customer_number is 6 digits
    timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")  # Current timestamp
    base_number_str = str(base_number).zfill(6)  # Ensure base_number is 6 digits to fit within the 19 digits limit
    reference_base = customer_number_str + timestamp_str + base_number_str
    reference_base = reference_base[:19]  # Truncate to ensure 19 digits if necessary
    check_digit = calculate_check_digit(reference_base)
    return reference_base + check_digit


def wrap_text(pdf, text, max_width):
    lines = []
    words = text.split()
    line = ""
    for word in words:
        if pdf.get_string_width(line + word + " ") <= max_width:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)
    return lines

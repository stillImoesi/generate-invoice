import csv
import os

def update_customer_number(
        file_path,
        customer_number,
        customer_type,
        contact_name,
        company_name,
        vat_number,
        email,
        street_address,
        postcode,
        city
    ):
    updated = False
    updated_rows = []

    # Read the existing data and update the matching row
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Read header if present
            if header:
                updated_rows.append(header)  # Preserve header

            for row in reader:
                if row[0] == customer_number:  # Check if the customer number matches
                    # Replace existing row with new details
                    row = [
                        customer_number,
                        customer_type,
                        company_name,
                        vat_number,
                        contact_name,
                        email,
                        street_address,
                        postcode,
                        city,
                        "Finland"  # Hardcoded as the country
                    ]
                    updated = True
                    print(f"Customer {customer_number} found. Updating details.")
                updated_rows.append(row)

    # If no matching customer number was found, add the new entry
    if not updated:
        updated_rows.append([
            customer_number,
            customer_type,
            company_name,
            vat_number,
            contact_name,
            email,
            street_address,
            postcode,
            city,
            "Finland"  # Hardcoded as the country
        ])
        print(f"No matching customer {customer_number} found. Adding as new customer.")

    # Write updated data back to the file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    if updated:
        print(f"Customer {customer_number} updated successfully.")
    else:
        print(f"New customer {customer_number} added successfully.")
import os
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv
from utils import (
    read_reference_number,
    write_reference_number,
    get_customer_number,
    update_customer_number,
    read_last_customer_number,
    generate_finnish_reference_number,
)
from validation import validate_finnish_reference_number
from create_invoice import PDF

# Load environment variables from .env file
load_dotenv()

# Read seller information from environment variables
seller_name = os.getenv('SELLER_NAME')
seller_address_line1 = os.getenv('SELLER_ADDRESS_LINE1')
seller_address_line2 = os.getenv('SELLER_ADDRESS_LINE2')
seller_country = os.getenv('SELLER_COUNTRY')
seller_business_id = os.getenv('SELLER_BUSINESS_ID')
seller_vat_number = os.getenv('SELLER_VAT_NUMBER')
seller_bank_account = os.getenv('SELLER_BANK_ACCOUNT')
seller_swift = os.getenv('SELLER_SWIFT')

# Check if all seller information is provided
if not all([seller_name, seller_address_line1, seller_address_line2, seller_country, seller_business_id, seller_vat_number, seller_bank_account, seller_swift]):
    print("Error: All seller information must be provided in the environment variables.")
    exit(1)

# File paths
ref_file = 'reference_number.txt'
customer_file = 'customer_number.csv'

# Setup argparse to handle inline arguments
parser = argparse.ArgumentParser(description='Generate an invoice.')
parser.add_argument('--skip_gen_cus_num', action='store_true', default=False, help='Skip generating a new customer number.')
parser.add_argument('--skip_gen_ref_num', action='store_true', default=False, help='Skip generating a new reference number.')
args = parser.parse_args()

# Prompting the user for input
customer_name = input("Enter customer name: ").strip()
customer_email = input("Enter customer email: ").strip()
customer_street_address = input("Enter customer street address: ").strip()
customer_postcode_city = input("Enter customer postcode and city: ").strip()
if not customer_name or not customer_email or not customer_street_address or not customer_postcode_city:
    print("Error: All address fields (customer name, customer email, street address, and postcode/city) are required.")
    exit(1)

# Get or generate customer number
if args.skip_gen_cus_num:
    customer_number = input("Enter customer number (at least 3 digits): ").strip()
    if not customer_number.isdigit() or len(customer_number) < 3:
        print("Error: Customer number must be at least 3 digits.")
        exit(1)
else:
    customer_number = get_customer_number(customer_file, customer_email)
    if customer_number is None:
        customer_number = read_last_customer_number(customer_file) + 1
        update_customer_number(customer_file, customer_email, customer_number)

# Collect multiple products, quantities, and prices
products = []
while True:
    product = input("Enter product description (or press enter to finish): ").strip()
    if not product:
        break

    quantity_input = input("Enter product quantity (default is 1): ").strip()
    try:
        quantity = int(quantity_input) if quantity_input else 1
    except ValueError:
        print("Error: Quantity must be a number. Defaulting to 1.")
        quantity = 1

    while True:
        price_input = input("Enter product price (including VAT): ").strip()
        try:
            total_price_with_vat = float(price_input)
            break
        except ValueError:
            print("Error: Price must be a number. Please try again.")

    price_without_vat = total_price_with_vat / 1.24
    vat_amount = total_price_with_vat - price_without_vat

    products.append((product, quantity, price_without_vat, vat_amount))

if not products:
    print("Error: At least one product is required.")
    exit(1)

invoice_date = input(f"Enter invoice date (default: {datetime.now().strftime('%Y-%m-%d')}): ").strip() or datetime.now().strftime("%Y-%m-%d")
due_date = (datetime.strptime(invoice_date, "%Y-%m-%d") + timedelta(days=14)).strftime("%Y-%m-%d")
message = input("Enter additional message: ").strip()

# Read the current reference number and update it
if args.skip_gen_ref_num:
    formatted_ref_number = input("Enter reference number (4-20 digits): ").strip()
    if not validate_finnish_reference_number(formatted_ref_number):
        print("Error: Invalid Finnish reference number.")
        exit(1)
else:
    base_number = read_reference_number(ref_file) + 10
    write_reference_number(ref_file, base_number)
    formatted_ref_number = generate_finnish_reference_number(customer_number, base_number)

# Create the directory structure
base_folder = 'customers'
customer_folder = os.path.join(base_folder, customer_name)
date_folder = os.path.join(customer_folder, invoice_date)
if not os.path.exists(customer_folder):
    os.makedirs(customer_folder)
if not os.path.exists(date_folder):
    os.makedirs(date_folder)

# Define the path to save the PDF
pdf_output_path = os.path.join(date_folder, f"{formatted_ref_number}.pdf")

# Create instance of PDF
pdf = PDF()

# Add the DejaVu font
pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf')
pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf')

# Add a page
pdf.add_page()

# Invoice details
invoice_details = [
    f"Asiakasnumero / Customer Number: {str(customer_number).zfill(6)}",
    f"Laskun numero / Invoice Number: {invoice_date.replace('-', '')}-001",
    f"Laskun päiväys / Invoice Date: {invoice_date}",
    f"Eräpäivä / Due Date: {due_date}"
]

pdf.add_invoice_details(invoice_details)

# Customer details
customer_details = [
    "Asiakas / Customer:",
    customer_email,
    customer_name,
    customer_street_address,
    customer_postcode_city,
    "Finland"
]

pdf.add_customer_details(customer_details)

# Seller details
seller_details = [
    "Myyjä / Seller:",
    seller_name,
    seller_address_line1,
    seller_address_line2,
    seller_country,
    f"Y-tunnus / Business ID: {seller_business_id}",
    f"ALV-numero / VAT Number: {seller_vat_number}"
]

pdf.add_seller_details(seller_details)

# Define column widths for the table
col_widths = [pdf.w / 3.5, pdf.w / 8, pdf.w / 5.5, pdf.w / 5.5]

# Add table
data = [
    ["Tuote / Service", "Määrä / Quantity", "Yksikköhinta / Unit Price", "Hinta / Price"]
]
total_without_vat = 0
total_vat = 0
total_with_vat = 0
for product, quantity, price_without_vat, vat_amount in products:
    total_without_vat += price_without_vat * quantity
    total_vat += vat_amount * quantity
    total_with_vat += (price_without_vat + vat_amount) * quantity
    data.append([product, str(quantity), f"{price_without_vat:.2f} €", f"{(price_without_vat + vat_amount) * quantity:.2f} €"])

data.append(["Alv / VAT (24%)", "", "", f"{total_vat:.2f} €"])
data.append(["Yhteensä / Total", "", "", f"{total_with_vat:.2f} €"])

pdf.add_table(data, col_widths)

# Add other details
other_details = [
    f"Viitenumero / Reference Number: {formatted_ref_number}",
    "Maksuehdot / Payment Terms: 14 päivää / 14 days",
    f"Tilinumero / Bank Account Number (IBAN): {seller_bank_account}",
    f"BIC / SWIFT: {seller_swift}",
    f"Viesti / Message: {message}"
]
pdf.add_invoice_details(other_details)

# Save the PDF
pdf.output(pdf_output_path)

print(f"Invoice saved to {pdf_output_path}")

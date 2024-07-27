import os
from datetime import datetime
from fpdf import FPDF, XPos, YPos
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read seller information from environment variables
seller_name = os.getenv('SELLER_NAME')
seller_address_line1 = os.getenv('SELLER_ADDRESS_LINE1')
seller_address_line2 = os.getenv('SELLER_ADDRESS_LINE2')
seller_country = os.getenv('SELLER_COUNTRY')
seller_business_id = os.getenv('SELLER_BUSINESS_ID')
seller_vat_number = os.getenv('SELLER_VAT_NUMBER')

# Check if all seller information is provided
if not all([seller_name, seller_address_line1, seller_address_line2, seller_country, seller_business_id, seller_vat_number]):
    print("Error: All seller information must be provided in the environment variables.")
    exit(1)

# Function to read the current reference number from a file
def read_reference_number(file_path):
    if not os.path.exists(file_path):
        return 10
    with open(file_path, 'r') as file:
        return int(file.read().strip())

# Function to write the new reference number to a file
def write_reference_number(file_path, ref_number):
    with open(file_path, 'w') as file:
        file.write(str(ref_number))

# Function to wrap text in a cell
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

# File to store the reference number
ref_file = 'reference_number.txt'

# Prompting the user for input
customer_name = input("Enter customer name: ").strip()
customer_street_address = input("Enter customer street address: ").strip()
customer_postcode_city = input("Enter customer postcode and city: ").strip()
if not customer_name or not customer_street_address or not customer_postcode_city:
    print("Error: All address fields (customer name, street address, and postcode/city) are required.")
    exit(1)

# Collect multiple products and prices
products = []
while True:
    product = input("Enter product description (or press enter to finish): ").strip()
    if not product:
        break

    while True:
        price_input = input("Enter product price (including VAT): ").strip()
        try:
            total_price_with_vat = float(price_input)
            break
        except ValueError:
            print("Error: Price must be a number. Please try again.")

    price_without_vat = total_price_with_vat / 1.24
    vat_amount = total_price_with_vat - price_without_vat

    products.append((product, price_without_vat, vat_amount))

if not products:
    print("Error: At least one product is required.")
    exit(1)

invoice_date = input(f"Enter invoice date (default: {datetime.now().strftime('%Y-%m-%d')}): ").strip() or datetime.now().strftime("%Y-%m-%d")
message = input("Enter additional message: ").strip()

# Read the current reference number and update it
ref_number = read_reference_number(ref_file)
new_ref_number = ref_number + 10
write_reference_number(ref_file, new_ref_number)

# Format the reference number to be 20 digits
formatted_ref_number = f"{new_ref_number:020}"

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

# Create PDF class
class PDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 9)
        self.cell(0, 10, 'LASKU / INVOICE', 0, new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')

    def add_invoice_details(self, details):
        self.set_font('DejaVu', '', 9)
        for line in details:
            self.cell(0, 5, line, 0, new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.ln()

    def add_customer_details(self, details):
        self.set_font('DejaVu', '', 9)
        for line in details:
            self.cell(0, 5, line, 0, new_x=XPos.LEFT, new_y=YPos.NEXT, align='R')
        self.ln()

    def add_table(self, data, col_widths):
        self.set_font('DejaVu', '', 9)
        row_height = self.font_size * 1.5
        for row in data:
            max_lines = 1
            wrapped_row = []
            for i, item in enumerate(row):
                wrapped_lines = wrap_text(self, str(item), col_widths[i])
                max_lines = max(max_lines, len(wrapped_lines))
                wrapped_row.append(wrapped_lines)

            for line in range(max_lines):
                for i, wrapped_lines in enumerate(wrapped_row):
                    if line < len(wrapped_lines):
                        self.multi_cell(
                            col_widths[i], row_height, wrapped_lines[line],
                            border=1, new_x=XPos.RIGHT, new_y=YPos.TOP,
                            max_line_height=self.font_size
                        )
                    else:
                        self.cell(col_widths[i], row_height, "", border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
                self.ln(row_height)
        self.ln()  # Add extra line after the table

# Create instance of PDF
pdf = PDF()

# Add the DejaVu font
pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf')
pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf')

# Add a page
pdf.add_page()

# Invoice details
invoice_details = [
    f"Laskun numero / Invoice Number: {invoice_date.replace('-', '')}-001",
    f"Laskun päiväys / Invoice Date: {invoice_date}",
    "Eräpäivä / Due Date: 14 päivää",
    "",
    "Myyjä / Seller:",
    seller_name,
    seller_address_line1,
    seller_address_line2,
    seller_country,
    f"Y-tunnus / Business ID: {seller_business_id}",
    f"ALV-numero / VAT Number: {seller_vat_number}"
]

customer_details = [
    "Asiakas / Customer:",
    customer_name,
    customer_street_address,
    customer_postcode_city,
    "Finland",
]

pdf.add_invoice_details(invoice_details)
pdf.add_customer_details(customer_details)

# Define column widths for the table
col_widths = [pdf.w / 3.5, pdf.w / 8, pdf.w / 5.5, pdf.w / 5.5]

# Add table
data = [
    ["Tuote / Service", "Määrä / Quantity", "Yksikköhinta / Unit Price", "Hinta / Price"]
]
total_without_vat = 0
total_vat = 0
total_with_vat = 0
for product, price_without_vat, vat_amount in products:
    total_without_vat += price_without_vat
    total_vat += vat_amount
    total_with_vat += price_without_vat + vat_amount
    data.append([product, "1", f"{price_without_vat:.2f} €", f"{(price_without_vat + vat_amount):.2f} €"])

data.append(["Alv / VAT (24%)", "", "", f"{total_vat:.2f} €"])
data.append(["Yhteensä / Total", "", "", f"{total_with_vat:.2f} €"])

pdf.add_table(data, col_widths)

# Add other details
other_details = [
    f"Viitenumero / Reference Number: {formatted_ref_number}",
    "Maksuehdot / Payment Terms: 14 päivää / 14 days",
    "Tilinumero / Bank Account Number (IBAN): FI16 5723 8120 3087 45",
    "BIC / SWIFT: OKOYFIHH",
    f"Viesti / Message: {message}"
]
pdf.add_invoice_details(other_details)

# Save the PDF
pdf.output(pdf_output_path)

print(f"Invoice saved to {pdf_output_path}")

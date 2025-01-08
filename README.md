# Invoice Generator

This script generates invoices in PDF format for customers, including details such as the seller's information, customer information, products, and prices (including VAT). The invoices are saved in a structured folder format based on the customer name and the date.

## Prerequisites

Make sure you have Python 3 installed on your system.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/invoice-generator.git
   cd invoice-generator
   ```

2. Create a virtual environment:

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

4. Create a new .env file in the root directory and add the following environment variables:

   ```plaintext
   SELLER_NAME=Your Company Name
   SELLER_ADDRESS_LINE1=Your Company Address Line 1
   SELLER_ADDRESS_LINE2=Your Company Address Line 2
   SELLER_COUNTRY=Your Company Country
   SELLER_BUSINESS_ID=Your Company Business ID
   SELLER_VAT_NUMBER=Your Company VAT Number
   SELLER_BANK_ACCOUNT=Your Company IBAN
   SELLER_SWIFT=Your Company SWIFT
   ```

5. If you want the code to maintain reference numbers, create a reference number file to keep track of the invoice numbers:

   ```plaintext
   reference_number.txt
   ```

   Add the initial reference number in the file. For example:

   ```plaintext
   10
   ```

6. Ensure that a `customer_number.csv` file exists in the root directory or will be generated automatically by the script if not present.

## Usage

Run the script to generate an invoice:

```sh
python index.py
```

### Selecting Customer Type

The script will prompt you to select whether the customer is a company or a private individual:

1. **Company Invoices**:
   - You will be prompted to enter the company name, VAT number, reference name (the person ordering the goods/services), and address details if they are missing from the `customer_number.csv`.
   - The selected or newly created customer’s details will be updated if any changes are made.

2. **Private Individual Invoices**:
   - You will be prompted to enter the individual’s name, email, and address details if they are missing from the `customer_number.csv`.
   - The script checks for missing details and prompts for them, ensuring existing records are updated only if necessary.

### Light CRM Functionality

This tool also acts as a light CRM (Customer Relationship Management) system by saving your customer data to a separate CSV file (`customer_number.csv`). This allows you to maintain and update customer information over time, ensuring that future invoices can be created quickly and efficiently without re-entering existing data.

### Collecting Product Details

The script will prompt you to enter product descriptions, quantities (default is 1 if not provided), and prices (including VAT). Prices entered will be automatically adjusted to show product prices without VAT.

### Saving the Invoice

The generated invoice will be saved in a folder structured as follows:

- `customers/<customer_name>/<date>/invoice.pdf`

## Arguments

The script accepts the following optional command-line arguments:

- `--skip_gen_cus_num`: Skip generating a new customer number. You will be prompted to enter the customer number manually.
- `--skip_gen_ref_num`: Skip generating a new reference number. You will be prompted to enter the reference number manually.

## Note

Ensure all seller information is provided in the `.env` file, as the script will fail if any information is missing.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.

# Invoice Generator

This script generates invoices in PDF format for customers, including details such as the seller's information, customer information, products, and prices (including VAT). The invoices are saved in a structured folder format based on the customer name and the date.

## Prerequisites

Make sure you have Python 3 installed on your system.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/invoice-generator.git
   cd invoice-generator

2. Create a virtual environment:

   ```sh
   python3 -m venv venv
   source venv/bin/activate

3. Install the required packages:

   ```sh
   pip install -r requirements.txt

4. Create a new .env file in the root directory and add the following environment variables:

   ```plaintext
   SELLER_NAME=Your Company Name
   SELLER_ADDRESS=Your Company Address
   SELLER_CITY=Your Company City
   SELLER_POSTAL_CODE=Your Company Postal Code
   SELLER_COUNTRY=Your Company Country
   SELLER_VAT_NUMBER=Your Company VAT Number
   SELLER_BANK_NAME=Your Company Bank Name
   SELLER_IBAN=Your Company IBAN
   SELLER_SWIFT=Your Company SWIFT
   SELLER_EMAIL=Your Company Email
   SELLER_PHONE=Your Company Phone

5. Create a reference number file to keep track of the invoice numbers (20 digits):

   ```plaintext
   00

## Usage

   ```sh
   python invoice_generator.py
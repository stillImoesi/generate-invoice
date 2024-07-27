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
        for row in reader:
            if row[0] == customer_email:
                return int(row[1])

    return None

def update_customer_number(file_path, customer_email, customer_number):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([customer_email, customer_number])

def read_last_customer_number(file_path):
    if not os.path.exists(file_path):
        return 1

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        last_row = None
        for last_row in reader:
            pass
        return int(last_row[1]) if last_row else 1

def calculate_check_digit(reference):
    weights = [7, 3, 1]
    total = 0
    for i, digit in enumerate(reversed(reference)):
        total += int(digit) * weights[i % 3]
    return str((10 - (total % 10)) % 10)


def generate_finnish_reference_number(base_number, customer_number):
    customer_number_str = str(customer_number).zfill(6)  # Ensure customer_number is 6 digits
    base_number_str = str(base_number).zfill(13)  # Ensure base_number is 13 digits
    reference_base = customer_number_str + base_number_str
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

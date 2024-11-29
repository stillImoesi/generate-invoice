from datetime import datetime

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
from utils import calculate_check_digit

def validate_finnish_reference_number(reference):
    if len(reference) < 4 or len(reference) > 20 or not reference.isdigit():
        return False
    expected_check_digit = calculate_check_digit(reference[:-1])
    return reference[-1] == expected_check_digit

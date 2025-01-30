import random
import string

def generate_random_code():
    letter1 = random.choice(string.ascii_uppercase)
    digit1 = random.choice(string.digits)
    letter2 = random.choice(string.ascii_uppercase)
    digits3 = ''.join(random.choices(string.digits, k=3))
    random_code = f"{letter1}{digit1}{letter2}{digits3}"
    return random_code


def generate_invoice_number(prefix="INV-"):
    random_number = ''.join(random.choices(string.digits, k=6))
    return f"{prefix}{random_number}"


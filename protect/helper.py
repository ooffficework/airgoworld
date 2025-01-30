import math
import requests
from datetime import datetime, timedelta
import random
import string
from .serializers import ProtectSerializer
from .models import Protect


def generate_random_code():
    letter1 = random.choice(string.ascii_uppercase)
    digit1 = random.choice(string.digits)
    letter2 = random.choice(string.ascii_uppercase)
    digits3 = ''.join(random.choices(string.digits, k=3))
    random_code = f"{letter1}{digit1}{letter2}{digits3}"
    return random_code


def create_protect_code(email):
    code = generate_random_code()
    data = {"code": code, "email": email}
    serializer = ProtectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return {
            "success": True,
            "code": code
        }
    return {
        "success": False,
        "code": None
    }
    
    
def check_protect_code(code, email):
    protect_code = Protect.objects.filter(email=email, code=code)
    if protect_code.exists():
        return True
    return False


def delete_protect_code(code, email):
    if not code or not email:
        return False
    protect_code = Protect.objects.get(email=email, code=code)
    if protect_code:
        protect_code.delete()
        return True
    return False
from django.utils.timezone import now, timedelta
from .models import OTP
from .serializers import OTPSerializer
import random
import requests
from django.conf import settings
from django.utils.timezone import now

def generate_otp():
    return str(random.randint(100000, 999999))


def verify_otp(email, code):
    if not email or not code:
        return {
            "success": False,
            "message": "Email and OTP code are required.",
        }
    otp = OTP.objects.filter(email=email, code=code).first()
    if otp:
        if otp.expiry < now():
            otp.delete()  
            return {"success": False, "message": "OTP has expired."}
        otp.delete()
        return {"success": True, "message": "OTP verified successfully!"}
    return {"success": False, "message": "Invalid OTP."}


def create_otp(email):
    if not email:
        return {"success": False, "message": "Please fill in your email"}
    code = generate_otp()
    expiry = now() + timedelta(minutes=10)
    data = {
        "email": email,
        "code": code,
        "expiry": expiry,
    }
    serializer = OTPSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return {
            "success": True,
            "message": "OTP generated successfully.",
            "data": serializer.data['code']
        }
    return {"success": False, "message": serializer.errors, "data": None}



def send_email(email, subject, message, text_content=None):
    try:
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "from": settings.RESEND_FROM_EMAIL, 
            "to": [email], 
            "subject": subject,
            "text": message, 
        }
        if text_content:
            payload["text"] = text_content  
        response = requests.post(url, json=payload, headers=headers)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)
        response.raise_for_status()  
        print("Email sent successfully:", response.json())  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send email: {e}")
        return None


import requests
from .serializers import OTPSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .helpers import generate_otp
from django.utils.timezone import now, timedelta
from .models import OTP
from rest_framework.permissions import AllowAny
from otp.helpers import send_email

class CreateOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data["email"]
        if not email:
            return Response(
                "Please fill in your email", status=status.HTTP_400_BAD_REQUEST
            )
        code = generate_otp()
        expires_at = now() + timedelta(minutes=10)
        print(code)
        data = {
            "email": email,
            "code": code,
            "expires_at": expires_at
        }
        serializer = OTPSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_email(email=email, subject="OTP", message=code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        if not email or not code:
            return Response(
                {"message": "Email and OTP code are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp = OTP.objects.filter(email=email, code=code).first()
        if otp:
            if otp.expires_at < now():
                otp.delete()
                return Response(
                    {"message": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST
                )
            otp.delete()
            return Response(
                {"message": "OTP verified successfully!"}, status=status.HTTP_200_OK
            )
        return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)



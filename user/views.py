from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from .models import CustomUser
from otp.helpers import create_otp, verify_otp
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.db import IntegrityError
from rest_framework import status
from django.contrib.auth import get_user_model
from core.helper import create_response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import CustomUser
User = get_user_model()


class VerifyUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        required_fields = ["email", "phone_number", "password", "firstname", "lastname"]
        data = request.data
        missing_fields = [field for field in required_fields if not data.get(field)]
        email = data.get("email", None)
        phone_number = data.get("phone_number", None)
        if missing_fields:
            return create_response(
                success=False,
                message="Please fill in all fields",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            validate_email(email)
        except ValidationError:
            return create_response(
                success=False,
                message="Invalid Email",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        if CustomUser.objects.filter(email=email).exists():
            return create_response(
                success=False,
                message="Email already exists",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return create_response(
                success=False,
                message="Phone Number already exists",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            otp = create_otp(email)
            print(otp)
            if not otp["success"]:
                return create_response(
                    success=False,
                    message="Failed to generate OTP",
                    http_status=status.HTTP_400_BAD_REQUEST,
                )
            return create_response(
                success=True,
                message="OTP sent successfully. Please check your email.",
                data=otp["data"],
                http_status=status.HTTP_200_OK,
            )
        except Exception as e:
            return create_response(
                success=False,
                message=f"An error occurred: {str(e)}",
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print(request.data)
        email = request.data.get("email")
        code = request.data.get("code")
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        if not email or not code:
            return create_response(
                success=False,
                message="Email and OTP code are required.",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        valid = verify_otp(email, code)
        if CustomUser.objects.filter(email=email).exists():
            return create_response(
                success=False,
                message="Email already exists",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return create_response(
                success=False,
                message="Phone Number already exists",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        if not valid.get("success"):
            return create_response(
                success=False,
                message="OTP verification failed.",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            get_user_model().objects.create_user(
                email=email,
                firstname=firstname,
                lastname=lastname,
                phone_number=phone_number,
                password=password,
            )
            return create_response(
                success=True,
                message="User created successfully!",
                http_status=status.HTTP_200_OK,
            )
        except IntegrityError as e:
            return create_response(
                success=False,
                message="A database error occurred. Please try again.",
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return create_response(
                success=False,
                message=f"An unexpected error occurred: {str(e)}",
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class RegisterSuperUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print(request.data)
        email = request.data.get("email")
        code = request.data.get("code")
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        if not email or not code:
            return create_response(
                success=False,
                message="Email and OTP code are required.",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        valid = verify_otp(email, code)
        if CustomUser.objects.filter(email=email).exists():
            return create_response(
                success=False,
                message="Email already exists",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return create_response(
                success=False,
                message="Phone Number already exists",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        if not valid.get("success"):
            return create_response(
                success=False,
                message="OTP verification failed.",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            get_user_model().objects.create_superuser(
                email=email,
                firstname=firstname,
                lastname=lastname,
                phone_number=phone_number,
                password=password,
            )
            return create_response(
                success=True,
                message="User created successfully!",
                http_status=status.HTTP_200_OK,
            )
        except IntegrityError as e:
            return create_response(
                success=False,
                message="A database error occurred. Please try again.",
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return create_response(
                success=False,
                message=f"An unexpected error occurred: {str(e)}",
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginUserView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return create_response(
                success=False,
                message="Email and password are required.",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(request, username=email, password=password)
        if not user:
            return create_response(
                success=False,
                message="Invalid email or password.",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return create_response(
            success=True,
            message="Login Successful",
            data={
                "refresh": str(refresh),
                "access": access_token,
            },
            http_status=status.HTTP_200_OK,
        )


class DeleteUserView(APIView):
    def delete(self, request, *args, **kwargs):
        email = kwargs.get("email")
        user = get_object_or_404(CustomUser, email=email)
        user.delete()
        return create_response(
            success=True,
            message="User Successfully Deleted",
            http_status=status.HTTP_200_OK,
        )

class JWTDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return create_response(
                success=False,
                message="Token is Required",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        token = token.split(" ")[1] if token.startswith("Bearer ") else token
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = CustomUser.objects.get(id=user_id)

            user_info = {
                "id": user.id,
                "email": user.email,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "phone_number": user.phone_number,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
            }
            return create_response(
                success=True,
                data=user_info,
                message="Details Fetched",
            )
        except CustomUser.DoesNotExist:
            return create_response(
                success=False,
                message="User not found",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return create_response(
                success=False,
                message="Invalid TOken",
                http_status=status.HTTP_400_BAD_REQUEST,
            )


class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get("email", None)
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        if not new_password or not confirm_password or not email:
            return create_response(
                success=False,
                http_status=status.HTTP_400_BAD_REQUEST,
                message="All fields are required.",
            )
        user = CustomUser.objects.get(email=email)
        if not user:
            return create_response(
                success=False,
                http_status=status.HTTP_400_BAD_REQUEST,
                message="Email not registered with an account",
            )
        if new_password != confirm_password:
            return create_response(
                success=False,
                http_status=status.HTTP_400_BAD_REQUEST,
                message="New password and confirm password do not match.",
            )
        if len(new_password) < 8:
            return  create_response(
                success=False,
                http_status=status.HTTP_400_BAD_REQUEST,
                message="Password must be at least 8 characters long.",
            )
        user.set_password(new_password)
        user.save()
        return create_response(
            success=True,
            http_status=status.HTTP_200_OK,
            message="Password updated successfully.",
        )


class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        if not current_password or not new_password or not confirm_password:
            return create_response(
                success=False,
                http_status=status.HTTP_400_BAD_REQUEST,
                message="All fields are required..",
            )

        if not user.check_password(current_password):
            return create_response(
                success=False,
                http_status=status.HTTP_400_BAD_REQUEST,
                message="Current password is incorrect...",
            )

        if new_password != confirm_password:
            return create_response(
                success=False,
                http_status=status.HTTP_400_BAD_REQUEST,
                message="New password and confirm password do not match.",
            )
        if len(new_password) < 8:
            return create_response(
                success=False,
                http_status=status.HTTP_400_BAD_REQUEST,
                message="Password must be at least 8 characters long.",
            )
        user.set_password(new_password)
        user.save()
        
        return create_response(
                success=True,
                http_status=status.HTTP_200_OK,
                message="Password updated successfully.",
            )

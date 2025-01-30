from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ValidationError

User = get_user_model()


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "firstname", "lastname", "phone_number", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError(
                {"success": False, "message": "Email already exists", "data": None}
            )
    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise ValidationError(
                {"success": False, "message": "Phone Number already exists", "data": None}
            )
        return value

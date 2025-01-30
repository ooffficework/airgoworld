from rest_framework import serializers
from .models import HotelBooking
from hotel.models import Hotel
from hotel.serializer import HotelSerializer


class CreateHotelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelBooking
        fields = "__all__"


class GetHotelBookingSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    class Meta:
        model = HotelBooking
        fields = "__all__"

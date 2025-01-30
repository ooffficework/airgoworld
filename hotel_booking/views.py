from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateHotelBookingSerializer, GetHotelBookingSerializer
from .models import HotelBooking
from hotel.models import Hotel
from user.models import CustomUser
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser
from core.helper import create_response
from hotel.models import Hotel
from .models import HotelBooking
from .serializers import CreateHotelBookingSerializer


class BookHotelView(APIView):
    def post(self, request):
        hotel = get_object_or_404(Hotel, id=request.data.get("hotel_id"))
        user = get_object_or_404(CustomUser, id=request.data.get("user_id"))
        rooms = int(request.data.get("rooms", 1))
        days = int(request.data.get("days", 1))
        print(request.data)
        if days < 0:
            return create_response(
                success=False,
                message="Please input a positive Number",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        price = hotel.price_per_night * rooms * days
        check_in_date_str = request.data.get("check_in_date")
        if not check_in_date_str:
            return Response(
                {"error": "Check-in date is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            check_in_date = datetime.strptime(
                check_in_date_str, "%Y-%m-%d"
            )  
            check_out_date = check_in_date + timedelta(days=days)
        except ValueError:
            return Response(
                {"error": "Invalid date format, use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            **request.data,
            "user": user.id,
            "hotel": hotel.id,
            "price": price,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
        }
        serialized_data = CreateHotelBookingSerializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            return create_response(
                success=True,
                data=serialized_data.data,
                message="Hotel Booked Successfully",
            )
        return create_response(
            success=True,
            message=serialized_data.errors,
            http_status=status.HTTP_400_BAD_REQUEST,
        )


    
class HotelBookingsView(APIView):
    def post(self, request):
        hotel_bookings = HotelBooking.objects.all()
        serialized_data = GetHotelBookingSerializer(hotel_bookings, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class HotelBookingDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        booking_id = kwargs.get("id")
        hotel_booking = get_object_or_404(HotelBooking, id=booking_id)
        serialized_data = GetHotelBookingSerializer(hotel_booking)
        return create_response(success=True, data=serialized_data.data, message='Fetched Successfully')

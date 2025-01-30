from rest_framework import status
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from decimal import Decimal
from .serializer import HotelSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .models import Hotel
from .add import create_hotels
from core.helper import create_response
class CreateHotelView(APIView):
    def post(self, request):
        try:
            price_per_night = Decimal(request.data.get("price_per_night"))
            rating = Decimal(request.data.get("rating"))
            images = [request.data.get("image")]
            data = {
                **request.data,
                "price_per_night": price_per_night,
                "rating": rating,
                "images": images,
            }
            serialized_hotel = HotelSerializer(data=data)
            if serialized_hotel.is_valid():
                serialized_hotel.save()
                return Response(serialized_hotel.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    serialized_hotel.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HotelDetailsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        hotel_id = kwargs.get("id")
        hotel = get_object_or_404(Hotel, id=hotel_id)
        serialized_hotel = HotelSerializer(hotel)
        return create_response(success=True, message='Fetched Successfully',data=serialized_hotel.data)


class AllHotelsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        hotel = Hotel.objects.all().order_by("-created_at")[1:5]
        serialized_hotels = HotelSerializer(hotel, many=True)
        return Response(serialized_hotels.data, status=status.HTTP_200_OK)


class DeleteHotelView(APIView):
    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if id == None:
            raise ValueError("Please input hotel id")
        hotel = get_object_or_404(Hotel, id=id)
        hotel.delete()
        return Response({"message": "Data deleted"}, status=status.HTTP_200_OK)


class SearchHotelView(APIView):
    def post(self, request, *args, **kwargs):
        location = request.data.get("location")
        hotels = Hotel.objects.filter(Q(city__icontains=location) | Q(state__icontains=location))
        data = HotelSerializer(hotels, many=True)
        return create_response(success=True, data=data.data, message='Fetched Successfully')
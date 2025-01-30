from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializer import CreateFlightBookingsSerializer, GetFlightBookingsSerializer
from django.shortcuts import get_object_or_404
from .models import BookFlight
from flight.models import Flight
from user.models import CustomUser
from decimal import Decimal
from rest_framework.permissions import AllowAny
from cabin.models import Cabin
from .helper import generate_random_code, generate_invoice_number
from django.shortcuts import get_object_or_404

class BookFlightView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            adults = int(request.data.get("adults", 0))
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            fullname = f"{firstname} {lastname}"
            children = int(request.data.get("children", 0))
            infants = int(request.data.get("infants", 0))
            amount = Decimal(request.data.get("amount", 0))
            user = get_object_or_404(CustomUser, id=request.data.get("user"))
            flight = get_object_or_404(Flight, id=request.data.get("flight"))
            cabin = get_object_or_404(Cabin, id=request.data.get("cabin"))
            booking_id = generate_random_code()
            pnr = generate_random_code()
            invoice_number = generate_invoice_number()
            data = {
                "booking_id": booking_id,
                "pnr": pnr,
                "invoice_number": invoice_number,
                "user": user.id,
                "flight": flight.id,
                "cabin": cabin.id,
                "adults": adults,
                "children": children,
                "fullname": fullname,
                "infants": infants,
                "amount": amount,
                **request.data,
            }
            print(data)  # Debugging the data being passed
            serializer = CreateFlightBookingsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Log validation errors to the console
                print("Validation Errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error:", str(e))  # Log the exception
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def get(self, request):
        booked_flights = BookFlight.objects.all()
        serializer = GetFlightBookingsSerializer(booked_flights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookingDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("booking_id")
        booking = get_object_or_404(BookFlight, id=id)
        serializer = GetFlightBookingsSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)


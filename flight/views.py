from rest_framework.response import Response
from django.db.models import OuterRef, Subquery
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timedelta
from .models import Flight
from .serializer import CreateFlightSerializer, GetFlightSerializer
from airport.models import Airport
from airline.models import Airline
from cabin.serializers import CabinSerializer
from cabin.models import Cabin
from django.shortcuts import get_object_or_404
from .helper import generate_flight_number, calculate_prices
import random
from .data import amenities
from core.helper import create_response
from rest_framework.permissions import AllowAny


class CreateFlight(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        required_fields = [
            "origin",
            "destination",
            "airline",
            "departure_date",
            "trip_type",
            "departure_time",
            "duration",
        ]
        for field in required_fields:
            if not request.data.get(field):
                return Response(
                    {"message": f"The field '{field}' is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            origin_airport = Airport.objects.get(id=request.data["origin"])
            destination_airport = Airport.objects.get(id=request.data["destination"])
            airline_obj = Airline.objects.get(id=request.data["airline"])
            if request.data["trip_type"] == "round":
                if not request.data.get("return_date"):
                    return Response(
                        {"message": "Return date is required for round trips."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return_date = datetime.strptime(request.data["return_date"], "%Y-%m-%d")
            else:
                return_date = None
        except (Airport.DoesNotExist, Airline.DoesNotExist) as e:
            return Response(
                {"message": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                {"message": f"ValueError: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        airlines = [airline_obj, airline_obj, airline_obj]
        fields = [1, 2, 3]
        departure_time = request.data["departure_time"]
        if int(departure_time[:2]) >= 0 and int(departure_time[:2]) <= 13:
            fields.pop(0)
        elif int(departure_time[:2]) >= 14 and int(departure_time[:2]) <= 20:
            fields.pop(1)
        else:
            fields.pop()
        minutes_list = ["00", "30", "45"]

        for index, airline_instance in enumerate(airlines):
            if index == 0:
                departure_date_str = (
                    f"{request.data['departure_date']} {departure_time}"
                )
                departure_date = datetime.strptime(departure_date_str, "%Y-%m-%d %H:%M")
            else:
                if 1 in fields:
                    rand = random.randint(0, 13)
                    hour = "00" if rand == 0 else f"{rand}"
                    time_str = f"{hour}:{random.choice(minutes_list)}"
                elif 2 in fields:
                    time_str = f"{random.randint(14, 20)}:{random.choice(minutes_list)}"
                elif 3 in fields:
                    time_str = f"{random.randint(21, 23)}:{random.choice(minutes_list)}"
                departure_date_str = f"{request.data['departure_date']} {time_str}"
                departure_date = datetime.strptime(departure_date_str, "%Y-%m-%d %H:%M")

            flight_number = (
                generate_flight_number()
            )  # Assume function to generate unique flight number
            flight_duration = request.data["duration"]
            multiplier = [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
            price_time_choice = random.choice(multiplier)
            duration = int(int(flight_duration[:2]) + price_time_choice * 10)
            flight_duration_hour = f"{duration}" if duration >= 10 else f"0{duration}"
            if index == 0:
                new_flight_duration = flight_duration
            else:
                new_flight_duration = (
                    f"{flight_duration_hour}:{flight_duration[3:5]}:00"
                )
            hours, minutes, seconds = map(int, new_flight_duration.split(":"))
            duration_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            arrival_date = departure_date + duration_delta
            data = {
                "origin": origin_airport.id,
                "destination": destination_airport.id,
                "airline": airline_instance.id,
                "departure_date": departure_date,
                "flight_duration": new_flight_duration,
                "arrival_date": arrival_date,
                "trip_type": request.data["trip_type"],
                "flight_number": flight_number,
            }

            if request.data["trip_type"] == "round":
                data["return_date"] = return_date
            base_prices = {
                "economy": (
                    int(request.data.get("economy"))
                    if index == 0
                    else int(request.data.get("economy")) * price_time_choice
                    + int(request.data.get("economy"))
                ),
                "business": (
                    int(request.data.get("business"))
                    if index == 0
                    else int(request.data.get("business")) * price_time_choice
                    + int(request.data.get("business"))
                ),
                "first": (
                    int(request.data.get("first"))
                    if index == 0
                    else int(request.data.get("first")) * price_time_choice
                    + int(request.data.get("first"))
                ),
                "vip": (
                    int(request.data.get("vip"))
                    if index == 0
                    else int(request.data.get("vip")) * price_time_choice
                    + int(request.data.get("vip"))
                ),
            }
            for cabin, price in base_prices.items():
                if price is None:
                    return Response(
                        {"message": f"The price for {cabin} is missing."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            serializer = CreateFlightSerializer(data=data)
            if serializer.is_valid():
                flight_instance = serializer.save()  # Save flight instance
                for key, (cabin_type, price) in enumerate(base_prices.items()):
                    Cabin.objects.create(
                        flight=flight_instance,
                        name=cabin_type,
                        prices=calculate_prices(price, 12.35, 17.50),
                        amenities=amenities[key],
                    )
            else:
                print(f"Flight {index+1} failed: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateFlight(APIView):
    def put(self, request, *args, **kwargs):
        data = request.data
        flight_id = kwargs.get("id")
        economy = int(data.get("economy", None))
        business = int(data.get("business", None))
        first = int(data.get("first", None))
        vip = int(data.get("vip", None))
        departure_time = data.get("departure_time", None)
        departure_date = data.get("departure_date", None)
        duration = data.get("duration", None)
        airline = data.get("airline", None)
        return_date = data.get("return_date", None)
        origin = data.get("origin", None)
        destination = data.get("destination", None)
        flight = get_object_or_404(Flight, id=flight_id)
        if airline:
            get_object_or_404(Airline, id=airline)
            flight.airline_id = airline
        if origin:
            get_object_or_404(Airport, id=origin)
            flight.origin_id = origin
        if destination:
            get_object_or_404(Airport, id=destination)
            flight.destination_id = destination
        if departure_date and departure_time:
            departure_date_str = f"{departure_date} {departure_time}"
            departure_date = datetime.strptime(departure_date_str, "%Y-%m-%d %H:%M")
            flight.departure_date = departure_date
        if departure_time and not departure_date:
            departure_date_str = f"{flight.departure_date.date()} {departure_time}"
            departure_date = datetime.strptime(departure_date_str, "%Y-%m-%d %H:%M")
            flight.departure_date = departure_date
        if duration:
            hours, minutes, seconds = map(int, duration.split(":"))
            flight.flight_duration = timedelta(
                hours=hours, minutes=minutes, seconds=seconds
            )
            flight.arrival_date = datetime.strptime(
                f"{flight.departure_date.date()} {flight.flight_duration}",
                "%Y-%m-%d %H:%M:%S",
            )
        if return_date:
            flight.return_date = datetime.strptime(f"{return_date}", "%Y-%m-%d")
            if flight.trip_type == "one_way":
                flight.trip_type = "round"
        flight_cabin = flight.cabin
        flight_cabin_serializer = CabinSerializer(flight_cabin, many=True)
        if economy:
            for cabin_class in flight_cabin_serializer.data:
                if cabin_class["name"] == "economy":
                    cabin = Cabin.objects.get(id=cabin_class["id"])
                    cabin.prices = calculate_prices(
                        economy, 12.35, 17.50, flight.trip_type
                    )
                    cabin.save()
        if business:
            for cabin_class in flight_cabin_serializer.data:
                if cabin_class["name"] == "business":
                    cabin = Cabin.objects.get(id=cabin_class["id"])
                    cabin.prices = calculate_prices(
                        business, 12.35, 17.50, flight.trip_type
                    )
                    cabin.save()
        if first:
            for cabin_class in flight_cabin_serializer.data:
                if cabin_class["name"] == "first":
                    cabin = Cabin.objects.get(id=cabin_class["id"])
                    cabin.prices = calculate_prices(
                        first, 12.35, 17.50, flight.trip_type
                    )
                    cabin.save()
        if vip:
            for cabin_class in flight_cabin_serializer.data:
                if cabin_class["name"] == "vip":
                    cabin = Cabin.objects.get(id=cabin_class["id"])
                    cabin.prices = calculate_prices(vip, 12.35, 17.50, flight.trip_type)
                    cabin.save()
        flight.save()
        return Response(GetFlightSerializer(flight).data, status=status.HTTP_200_OK)


class AllFlightsView(APIView):
    permission_classes = [
        AllowAny
    ]  # Override default permission classes to allow public access

    def get(self, request):
        flights = Flight.objects.prefetch_related("cabin").all()
        serializer = GetFlightSerializer(flights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchFlight(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Flight.objects.all().delete()
        origin_iata = request.data.get("origin")
        destination_iata = request.data.get("destination")
        departure_date = request.data.get("departure_date")
        get_object_or_404(Airport, iata=origin_iata)
        get_object_or_404(Airport, iata=destination_iata)
        flight = Flight.objects.filter(
            origin__iata__icontains=origin_iata,
            destination__iata__icontains=destination_iata,
        )
        if not flight.exists():
            return Response([], status=status.HTTP_200_OK)
        serializer = GetFlightSerializer(flight, many=True)
        serializer_data = serializer.data
        for flight in serializer_data:
            flight_time = flight["departure_date"][11:16]
            date_added_with_time = f"{departure_date} {flight_time}"
            converted_date = datetime.strptime(date_added_with_time, "%d-%m-%Y %H:%M")
            flight["departure_date"] = converted_date
            flight_instance = Flight.objects.get(id=flight["id"])
            serializer = GetFlightSerializer(flight_instance, data=flight, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        origin_iata = kwargs.get("origin")
        destination_iata = kwargs.get("destination")
        departure_date = kwargs.get("departure_date")
        ddate = datetime.strptime(departure_date, "%d-%m-%Y")
        get_object_or_404(Airport, iata=origin_iata)
        get_object_or_404(Airport, iata=destination_iata)
        print(kwargs)
        flight = Flight.objects.filter(
            origin__iata__icontains=origin_iata,
            destination__iata__icontains=destination_iata,
        )
        if not flight:
            return Response([], status=status.HTTP_200_OK)
        serializer = GetFlightSerializer(flight, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FlightDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        flight = get_object_or_404(Flight, id=id)
        serializer = GetFlightSerializer(flight)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FlightToDisplayView(APIView):
    def get(self, request):
        subquery = (
            Flight.objects.filter(
                origin=OuterRef("origin"), destination=OuterRef("destination")
            )
            .order_by("id")
            .values("id")[:1]
        )
        unique_flights = Flight.objects.filter(id__in=Subquery(subquery))
        serializer = GetFlightSerializer(unique_flights, many=True)
        return create_response(
            success=True, message="Flights Fetch", data=serializer.data
        )

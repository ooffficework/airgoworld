
class SearchFlight(APIView):
    def get(self, request, *args, **kwargs):
        origin = kwargs.get('origin')
        destination = kwargs.get('destination')
        departure_date = kwargs.get('departure_date')
        trip_type = kwargs.get('trip_type')
        
        if all([origin, destination, departure_date]):
            try:
                origin_airport = Airport.objects.get(iata=origin)
                destination_airport = Airport.objects.get(iata=destination)
                departure_date = datetime.strptime(departure_date, "%d-%m-%Y").date()
                existing_flight = Flight.objects.filter(
                    origin=origin_airport,
                    destination=destination_airport,
                    departure_date__date=departure_date
                ).first()

                if existing_flight:
                    return Response([CreateFlightSerializer(existing_flight).data], status=status.HTTP_200_OK)
                current_time = datetime.now()
                departure_time = (current_time + timedelta(hours=6)).strftime("%H:%M")
                departure_date_str = f"{departure_date} {departure_time}"
                departure_date = datetime.strptime(departure_date_str, "%Y-%m-%d %H:%M")
                duration_delta = timedelta(hours=6, minutes=30)
                adate = departure_date + duration_delta
                flight_number = generate_flight_number()
                random_airline_id = random.randint(1, 10)
                
                data = {
                    "origin": origin_airport.id,
                    "destination": destination_airport.id,
                    "airline": random_airline_id,
                    "departure_date": departure_date,
                    "flight_duration": "6:30",  # Example duration
                    "arrival_date": adate,
                    "trip_type": trip_type,
                    "flight_number": flight_number,
                }
                base_prices = {
                    "economy": 2000,
                    "business": 3200,
                    "first": 4500,
                    "vip": 6500,
                }
                serializer = CreateFlightSerializer(data=data)
                if serializer.is_valid():
                    flight_instance = serializer.save()
                    for index, cabin_type in enumerate(["economy", "business", "first", "vip"]):
                        Cabin.objects.create(
                            flight=flight_instance,
                            name=cabin_type,
                            prices=calculate_prices(base_prices[cabin_type], 12.35, 17.50,trip_type),
                            amenities=amenities[index]
                        )
                    return Response([serializer.data], status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Airport.DoesNotExist as e:
                return Response({"message": f"Airport error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {"message": "The fields 'origin', 'destination', and 'departure_date' are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    
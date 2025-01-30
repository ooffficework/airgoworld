from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Car
from .serializers import CarSerializer
from .add import create_cars
from hotel.add import create_hotels
from airport.add import add_airports 
from airline.add import add_airlines 
from tours.add import create_mock_data

class CreateCarView(APIView):
    def post(self, request):
        rental_price = int(request.data.get('rental_price', 0))
        data  = {**request.data, "rental_price": rental_price}
        print(request.data)
        serializer =  CarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class GetCarsView(APIView):
    def get(self, request):
        # create_mock_data()
        # create_hotels()
        # add_airlines()
        # add_airports()
        # create_cars()
        cars =  Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

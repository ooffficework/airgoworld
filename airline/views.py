from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializer import AirlineSerializer
from .models import Airline
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .add import add_airlines
class AirlineView(APIView):
    permission_classes = [AllowAny]  
    def post(self, request):
        serializer = AirlineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    def get(self, request):
        airlines = Airline.objects.all()
        serialized_airlines = AirlineSerializer(airlines, many=True)
        return Response(serialized_airlines.data, status=status.HTTP_200_OK) 
        
class AirlineDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        airline_id = kwargs.get('id')
        airline = get_object_or_404(Airline, id=airline_id)
        serialized_airline = AirlineSerializer(airline)
        return Response(serialized_airline.data, status=status.HTTP_200_OK) 
        
        
class DeleteAirlineView(APIView):
    def delete(self, request, *args, **kwargs):
        airline_id = kwargs.get('id')
        airline = get_object_or_404(Airline, id=airline_id)
        airline.delete()
        return Response({"message": "Airline Successfully Deleted"}, status=status.HTTP_200_OK) 
class SelectAirlineView(APIView):
    def get(self, request):
        airlines = Airline.objects.all()
        serializer = AirlineSerializer(airlines, many=True)
        return_data = [{"value": "", "label": ""}]
        print(serializer.data)
        for airline in serializer.data:
            data = {
                "label": f"{airline['name']}",
                "value": airline['id']
            }
            return_data.append(data)
        return Response(return_data, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from .serializer import AirportSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Airport
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .add import add_airports
from rest_framework.permissions import AllowAny

class AirportView(APIView):
    permission_classes = [AllowAny]  
    def post(self, request):
        serialized_airport = AirportSerializer(data=request.data)
        if serialized_airport.is_valid():
            serialized_airport.save()
            return Response(serialized_airport.data, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'message': 'Validation failed',
            'data': serialized_airport.errors
        }, status=400)
    def get(self, request):
        airports = Airport.objects.all()
        serialized_airports = AirportSerializer(airports, many=True)
        return Response(serialized_airports.data, status=status.HTTP_200_OK)
    
from rest_framework.pagination import LimitOffsetPagination

class SearchAirportView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        query = kwargs.get("query", "").strip()
        if query == "":
            airports = Airport.objects.all()
        else:
            airports = Airport.objects.filter(
                Q(name__icontains=query) | Q(city__icontains=query) | Q(country__icontains=query)
            )
        serialized_airports = AirportSerializer(airports, many=True)
        return Response(serialized_airports.data, status=status.HTTP_200_OK)


class AirportDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        airport_id =  kwargs.get('id')
        airport = get_object_or_404(Airport, id=airport_id)
        serialized_airport = AirportSerializer(airport)
        return Response(serialized_airport.data, status=status.HTTP_200_OK)

        
class DeleteAirportView(APIView):
    def delete(self, request, *args, **kwargs):
        airport_id = kwargs.get('id')
        airport = get_object_or_404(Airport, id=airport_id)
        airport.delete()
        return Response({"message": "airport Successfully Deleted"}, status=status.HTTP_200_OK) 
        
class SelectAirportView(APIView):
    def get(self, request):
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)
        return_data = [{"value": "", "label": ""}]
        print(return_data)
        for flight in serializer.data:
            data = {
                "label": f"{flight['name']} - {flight['country']}",
                "value": flight['id']
            }
            return_data.append(data)
        return Response(return_data, status=status.HTTP_200_OK)
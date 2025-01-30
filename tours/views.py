from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateTourSerializer,GetTourSerializer
from .models import Tour
from django.shortcuts import get_object_or_404
from .add import create_mock_data

class CreateTourView(APIView):
    def post(self, request):
        serialized_data = CreateTourSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
class GetToursView(APIView):
    def get(self, request):
        tours = Tour.objects.filter(display=True)
        serialized_data = GetTourSerializer(tours, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    
class DeleteTourView(APIView): 
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        tour = get_object_or_404(Tour, id=id)
        tour.delete()
        return Response('Tour Deleted', status=status.HTTP_200_OK)
        
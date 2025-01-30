from rest_framework.views import APIView
from .serializer import StoreRoomSerializer, RetrieveRoomSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Room
from django.shortcuts import get_object_or_404
from hotel.models import Hotel


class CreateRoomView(APIView):
    def post(self, request):
        serialized_room = StoreRoomSerializer(data=request.data)
        if serialized_room.is_valid():
            serialized_room.save()
            return Response(serialized_room.data, status=status.HTTP_201_CREATED)
        return Response(serialized_room.errors, status=status.HTTP_400_BAD_REQUEST)


class AllRoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serialized_rooms = RetrieveRoomSerializer(rooms, many=True)
        return Response(serialized_rooms.data, status=status.HTTP_200_OK)


class RoomDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        room_id = kwargs.get("id")
        room = get_object_or_404(Room, id=room_id)
        serialized_room = RoomSerializer(room)
        return Response(serialized_room.data, status=status.HTTP_200_OK)


class DeleteRoomView(APIView):
    def delete(self, request, *args, **kwargs):
        room_id = kwargs.get("id")
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        return Response(
            {"message": "Room deleted successfully"}, status=status.HTTP_200_OK
        )

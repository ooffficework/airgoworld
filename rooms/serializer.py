from rest_framework import serializers
from .models import Room
from hotel.serializer import HotelSerializer  
from hotel.models import Hotel

class StoreRoomSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all(), write_only=True
    )  
    class Meta:
        model = Room
        fields = "__all__"
        
class RetrieveRoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)   
    class Meta:
        model = Room
        fields = "__all__"
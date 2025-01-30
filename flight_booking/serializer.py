from rest_framework import serializers
from flight.serializer import GetFlightSerializer
from cabin.serializers import CabinSerializer
from flight.models import Flight
from .models import BookFlight
class CreateFlightBookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFlight
        fields = "__all__"
        
class GetFlightBookingsSerializer(serializers.ModelSerializer):
    flight = GetFlightSerializer(read_only=True)
    cabin = CabinSerializer(read_only=True)
    class Meta:
        model = BookFlight
        fields = "__all__"
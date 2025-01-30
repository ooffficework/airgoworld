from airport.serializer import AirportSerializer
from airline.serializer import AirlineSerializer
from rest_framework import serializers
from airline.models import Airline
from airport.models import Airport
from .models import Flight
from cabin.serializers import CabinSerializer

class CreateFlightSerializer(serializers.ModelSerializer):
    airline = serializers.PrimaryKeyRelatedField(
        queryset=Airline.objects.all(), write_only=True
    )
    origin = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    destination = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )

    def validate(self, attrs):
        origin = attrs.get("origin")
        destination = attrs.get("destination")
        if origin == destination:
            raise serializers.ValidationError(
                "Origin and Destination cannot be the same"
            )
        return attrs

    class Meta:
        model = Flight
        fields = "__all__"


class GetFlightSerializer(serializers.ModelSerializer):
    airline = AirlineSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)
    origin = AirportSerializer(read_only=True)
    cabin = CabinSerializer(many=True, read_only=True)
    class Meta:
        model = Flight
        fields = "__all__"



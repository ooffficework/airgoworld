from rest_framework import serializers
from .models import Airport

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name', 'city', 'country', 'iata', 'scope', 'active', 'status']
    
    def validate(self, data):
        if Airport.objects.filter(
            country=data['country'],
            city=data['city'],
            name=data['name'],
            scope=data['scope'],
            iata=data['iata']
        ).exists():
            raise serializers.ValidationError("An airport with this combination already exists.")
        return data

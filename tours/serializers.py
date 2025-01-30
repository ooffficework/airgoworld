from rest_framework import serializers
from .models import Tour


class CreateTourSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tour
        fields = "__all__"
        
class GetTourSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tour
        fields = "__all__"
        
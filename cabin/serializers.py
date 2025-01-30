from rest_framework import serializers
from .models import Cabin

class CabinSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Cabin
        fields = "__all__"

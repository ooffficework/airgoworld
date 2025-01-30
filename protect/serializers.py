from rest_framework import serializers
from .models import Protect


class ProtectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protect
        fields = '__all__'
        
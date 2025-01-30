from rest_framework import serializers

from .models import BankInfo


class BankInfoSerializers(serializers.ModelSerializer):
    class Meta: 
        model = BankInfo
        fields = "__all__"
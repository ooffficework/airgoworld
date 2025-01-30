from django.shortcuts import render
from .serializers import BankInfoSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BankInfo
from rest_framework import status
from django.shortcuts import get_object_or_404


class CreateBankView(APIView):
    def post(self, request):
        serializer = BankInfoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllBankInfosView(APIView):
    def get(self, request):
        bank_infos = BankInfo.objects.all()
        serializer = BankInfoSerializers(bank_infos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request, *args, **kwargs):
        bank_info = get_object_or_404(BankInfo, id=kwargs.get("id"))
        bank_info.delete()
        return Response(
            {"message": "Data Successfully Deleted"}, status=status.HTTP_200_OK
        )
    def patch(self, request, *args, **kwargs):
        bank_info_id = kwargs.get("id")
        serializer = BankInfoSerializers(bank_info_id, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

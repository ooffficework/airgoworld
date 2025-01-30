from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentMethod
from core.helper import create_response
from django.shortcuts import get_object_or_404
from .serializers import PaymentMethodSerializer

class PaymentMethodCreateView(APIView):
    def post(self, request):
        serializer = PaymentMethodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        payment_methods = PaymentMethod.objects.filter(display=True)
        serializer = PaymentMethodSerializer(payment_methods, many=True)
        return create_response(success=True, data=serializer.data, message='Data Fetched Successfully')

class UpdatePaymentMethod(APIView):
    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        name = request.data.get('name', None)
        is_active = request.data.get('is_active', None)
        details = request.data.get('details', None)
        display = request.data.get('display', None)
        payment_method = get_object_or_404(PaymentMethod, id=id)
        if name:
            payment_method['name'] = name 
        if is_active:
            payment_method['is_active'] = is_active 
        if display:
            payment_method['display'] = display 
        if details:
            payment_method['details'] = {**payment_method['details'], **details}
        payment_method.save()
        serializer = PaymentMethodSerializer(payment_method)
        return create_response(serializer.data, message='Data Fetched Successfully')

        
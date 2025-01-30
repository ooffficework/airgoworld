from django.urls import path
from .views import PaymentMethodCreateView, UpdatePaymentMethod

urlpatterns = [
    path('create/', PaymentMethodCreateView.as_view(), name='create-payment-method'),
    path('get/', PaymentMethodCreateView.as_view(), name='all-payment-method'),
    path('update/<int:id>/', UpdatePaymentMethod.as_view(), name='update-payment-method'),
]

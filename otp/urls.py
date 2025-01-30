from django.urls import path
from .views import CreateOTP, VerifyOTP

urlpatterns = [
    path('create/', CreateOTP.as_view()),
    path('verify/', VerifyOTP.as_view()),
]

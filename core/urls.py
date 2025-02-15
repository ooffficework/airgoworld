"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('blog/', include('blog.urls')),
    path('airline/', include('airline.urls')),
    path('airport/', include('airport.urls')),
    path('hotel/', include('hotel.urls')),
    path('hotel/', include('hotel_booking.urls')),
    path('room/', include('rooms.urls')),
    path('tours/', include('tours.urls')),
    path('car/', include('car.urls')),
    path('flight/', include('flight.urls')),
    path('flight/', include('flight_booking.urls')),
    path('otp/', include('otp.urls')),
    path('bank/', include('bank_infos.urls')),
    path('payment-methods/', include('paymentmethod.urls')),
]

from django.urls import path
from .views import BookHotelView, HotelBookingDetailsView

urlpatterns = [
    path('book/', BookHotelView.as_view()),
    path('book/details/<int:id>/', HotelBookingDetailsView.as_view())
]

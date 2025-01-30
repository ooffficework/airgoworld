from django.urls import path
from .views import BookFlightView, BookingDetailsView

urlpatterns = [
    path('book/', BookFlightView.as_view()),
    path('book/all/', BookFlightView.as_view()),
    path('book/details/<int:booking_id>/', BookingDetailsView.as_view())
]

from django.urls import path
from .views import CreateFlight, AllFlightsView, SearchFlight, FlightDetailsView, UpdateFlight, FlightToDisplayView

urlpatterns = [
    path('create/', CreateFlight.as_view()),
    path('all/', AllFlightsView.as_view()),
    path('display/', FlightToDisplayView.as_view()),
    path('search/', SearchFlight.as_view()),
    path('update/<int:id>/', UpdateFlight.as_view()),
    path('search/<str:origin>/<str:destination>/<str:departure_date>/<str:trip_type>/', SearchFlight.as_view()),
    path('details/<int:id>/', FlightDetailsView.as_view(), name='flight-detail'),
]

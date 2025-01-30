from django.urls import path
from .views import AirportView,AirportDetailsView, SearchAirportView, SelectAirportView, DeleteAirportView

urlpatterns = [
    path('create/', AirportView.as_view()),
    path('search/<str:query>/', SearchAirportView.as_view()),
    path('all/', AirportView.as_view()),
    path('details/<int:id>/', AirportDetailsView.as_view()),
    path('delete/<int:id>/', DeleteAirportView.as_view()),
    path('select/', SelectAirportView.as_view()),
]

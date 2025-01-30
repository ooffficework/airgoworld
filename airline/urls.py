from django.urls import path 
from .views import AirlineView, AirlineDetailsView, SelectAirlineView, DeleteAirlineView
urlpatterns = [
    path('create/', AirlineView.as_view()),
    path('all/', AirlineView.as_view()),
    path('details/<int:id>/', AirlineDetailsView.as_view()),
    path('delete/<int:id>/', DeleteAirlineView.as_view()),
    path('select/', SelectAirlineView.as_view())
]

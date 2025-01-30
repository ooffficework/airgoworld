from django.urls import path
from .views import CreateHotelView, AllHotelsView, HotelDetailsView, DeleteHotelView, SearchHotelView

urlpatterns = [
    path('details/<int:id>/', HotelDetailsView.as_view()),
    path('create/', CreateHotelView.as_view()),
    path('all/', AllHotelsView.as_view()),
    path('search/', SearchHotelView.as_view()),
    path('delete/<int:id>/', DeleteHotelView.as_view())
]

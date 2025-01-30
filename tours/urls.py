from django.urls import path

from .views import CreateTourView,GetToursView,DeleteTourView

urlpatterns = [
    path('create/', CreateTourView.as_view()),
    path('all/', GetToursView.as_view()),
    path('delete/<int:id>/', DeleteTourView.as_view())
]

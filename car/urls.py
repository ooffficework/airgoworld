from django.urls import path

from .views import CreateCarView, GetCarsView

urlpatterns = [
    path("create/", CreateCarView.as_view()),
    path("all/", GetCarsView.as_view()),
]

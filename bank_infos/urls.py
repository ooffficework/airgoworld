from django.urls import path
from .views import CreateBankView, GetAllBankInfosView

urlpatterns = [
    path("all/", GetAllBankInfosView.as_view()),
    path("create/", CreateBankView.as_view()),
]

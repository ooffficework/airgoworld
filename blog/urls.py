from django.urls import path
from .views import BlogsView



urlpatterns = [
    path('create/', BlogsView.as_view()),
    path('update/<int:id>', BlogsView.as_view())
]
from django.urls import path
from .views import CreateRoomView, AllRoomsView, DeleteRoomView, RoomDetailsView

urlpatterns = [
    path("details/<int:id>/", RoomDetailsView.as_view()),
    path("delete/<int:id>/", DeleteRoomView.as_view()),
    path("create/", CreateRoomView.as_view()),
    path("all/", AllRoomsView.as_view()),
]

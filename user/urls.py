from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    JWTDetailsView,
    RegisterSuperUserView,
    VerifyUserView,
    DeleteUserView,
    ChangePasswordView,
    UpdatePasswordView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("register/admin/", RegisterSuperUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", VerifyUserView.as_view(), name="verify"),
    path("delete/<str:email>/", DeleteUserView.as_view(), name="delete"),
    path("jwt_details/", JWTDetailsView.as_view(), name="jwt-details"),
    path("password-change/", ChangePasswordView.as_view(), name="change-password"),
    path("password-update/", UpdatePasswordView.as_view(), name="update-password"),
]

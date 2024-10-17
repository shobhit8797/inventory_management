# auth/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyTokenObtainPairView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # User Registration
    path(
        "login/", MyTokenObtainPairView.as_view(), name="login"
    ),  # Login (Token obtain)
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Refresh Token
]

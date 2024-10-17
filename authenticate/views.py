# auth/views.py
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer


# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    permission_classes = (AllowAny,)  # Allow any user to register


# JWT Token Management (Login and Refresh)
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)  # Allow any user to log in

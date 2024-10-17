# inventory/urls.py
from django.urls import path

from .views import ItemDetailView, ItemView

urlpatterns = [
    path("items/", ItemView.as_view(), name="item-create"),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
]

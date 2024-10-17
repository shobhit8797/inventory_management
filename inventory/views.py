# inventory/views.py
import logging

from django.core.cache import cache
from rest_framework import generics
from rest_framework.response import Response

from .models import Item
from .serializers import ItemSerializer

logger = logging.getLogger("inventory")


class ItemView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        logger.info("Item creation requested by user %s", request.user)
        try:
            response = super().create(request, *args, **kwargs)
            logger.info("Item created successfully: %s", response.data)
            return response
        except Exception as e:
            logger.error("Error while creating item: %s", str(e))
            raise


class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def retrieve(self, request, *args, **kwargs):
        item_id = kwargs.get("pk")
        logger.debug("Retrieving item with ID %s", item_id)

        cached_item = cache.get(f"item_{item_id}")
        if cached_item:
            logger.info("Cache hit for item %s", item_id)
            return Response(cached_item)

        logger.info("Cache miss for item %s. Fetching from database.", item_id)
        try:
            item = self.get_object()
            serializer = self.get_serializer(item)
            cache.set(f"item_{item_id}", serializer.data, timeout=3600)
            logger.info("Item %s retrieved and cached.", item_id)
            return Response(serializer.data)
        except Item.DoesNotExist:
            logger.error("Item %s not found.", item_id)
            return Response({"error": "Item not found"}, status=404)

    def patch(self, request, *args, **kwargs):
        item_id = kwargs.get("pk")
        logger.info("Updating item with ID %s", item_id)

        try:
            response = super().patch(request, *args, **kwargs)
            cache.set(f"item_{item_id}", response.data, timeout=3600)
            logger.info("Item %s updated and cache refreshed.", item_id)
            return response
        except Exception as e:
            logger.error("Error while updating item %s: %s", item_id, str(e))
            raise

    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get("pk")
        logger.info("Deleting item with ID %s", item_id)

        try:
            response = super().delete(request, *args, **kwargs)
            cache.delete(f"item_{item_id}")
            logger.info("Item %s deleted and removed from cache.", item_id)
            return response
        except Exception as e:
            logger.error("Error while deleting item %s: %s", item_id, str(e))
            raise

# inventory/tests.py
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Item

User = get_user_model()


class ItemViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        self.url = reverse("item-create")
        self.valid_payload = {
            "name": "New Item",
            "description": "A description for the new item",
            "quantity": 20,
            "price": "29.99",
        }
        self.invalid_payload = {
            "name": "",  # Invalid name
            "description": "Invalid item",
            "quantity": -5,  # Invalid quantity
            "price": "9.99",
        }
        # Create some items for list retrieval tests
        self.item1 = Item.objects.create(
            name="Item 1", description="Description 1", quantity=10, price="19.99"
        )
        self.item2 = Item.objects.create(
            name="Item 2", description="Description 2", quantity=5, price="9.99"
        )

    def test_create_item_success(self):
        """Test creating a new item successfully"""
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(
            Item.objects.count(), 3
        )  # Two items created in setUp and one more

    def test_create_item_invalid(self):
        """Test creating a new item with invalid data"""
        response = self.client.post(self.url, self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Item.objects.count(), 2)  # No new items should be created

    def test_list_items_success(self):
        """Test retrieving the list of items"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two items created in setUp
        self.assertEqual(response.data[0]["name"], "Item 1")
        self.assertEqual(response.data[1]["name"], "Item 2")


class ItemDetailTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.item = Item.objects.create(
            name="Test Item", description="Test description", quantity=10, price="9.99"
        )
        cls.detail_url = reverse("item-detail", kwargs={"pk": cls.item.id})

    def setUp(self):
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        cache.clear()  # Clear the cache before each test

    def test_get_item_success(self):
        """Test retrieving an item successfully"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.item.name)

    def test_get_item_not_found(self):
        """Test retrieving a non-existent item"""
        non_existent_url = reverse("item-detail", kwargs={"pk": 999})
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item_success(self):
        """Test updating an existing item"""
        update_payload = {
            "name": "Updated Item",
            "description": "Updated description",
            "quantity": 15,
            "price": "19.99",
        }
        response = self.client.patch(self.detail_url, update_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated Item")

    def test_delete_item_success(self):
        """Test deleting an item"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_delete_item_not_found(self):
        """Test deleting a non-existent item"""
        non_existent_url = reverse("item-detail", kwargs={"pk": 999})
        response = self.client.delete(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

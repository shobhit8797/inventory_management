# inventory/models.py
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

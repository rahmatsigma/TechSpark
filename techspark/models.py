# techspark/models.py

from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0) # Harga dalam Rupiah
    image_url = models.URLField(max_length=1000) 
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
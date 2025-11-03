# techspark/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# ================================
#  ▼▼▼ CLASS CATEGORY (BARU) ▼▼▼
# ================================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# ================================
#  ▼▼▼ CLASS PRODUCT (UPDATE) ▼▼▼
# ================================
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image_url = models.URLField(max_length=1000)
    stock = models.IntegerField(default=10)
    
    # ▼▼▼ INI FIELD YANG HILANG ▼▼▼
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# ================================
#  ▼▼▼ SISANYA (Cart & CartItem) ▼▼▼
# ================================
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Keranjang milik {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} di {self.cart.user.username}"
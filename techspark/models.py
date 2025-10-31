from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0) # Harga dalam Rupiah
    image_url = models.URLField(max_length=1000) 
    created_at = models.DateTimeField(default=timezone.now)
    stock = models.IntegerField(default=10)

    def __str__(self):
        return self.name
    
# 1. Model untuk Keranjang Belanja 
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Keranjang milik {self.user.username}"

# 2. Model untuk Item di dalam Keranjang
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    # Properti untuk menghitung subtotal
    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} di {self.cart.user.username}"
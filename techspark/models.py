# techspark/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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
    


    # 1. Model untuk Alamat Pengiriman
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"Alamat {self.full_name} ({self.user.username})"
    
    class Meta:
        verbose_name_plural = "Addresses"

# 2. Model untuk Pesanan (Order)
class Order(models.Model):
    # --- Status Choices ---
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Sedang Diproses'),
        ('shipped', 'Dikirim'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    shipping_address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=0)
    
    PAYMENT_CHOICES = [
        ('cod', 'Cash On Delivery (COD)'),
        ('qris', 'QRIS'),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')
    
    # ▼▼▼ TAMBAHKAN FIELD INI ▼▼▼
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} oleh {self.user.username}"

# ==================================
#  ▼▼▼ 2. UPDATE MODEL ORDERITEM ▼▼▼
# ==================================
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    
    # ▼▼▼ TAMBAHKAN LINK ASLI KE PRODUK ▼▼▼
    # Ini penting untuk rating & jika produk dihapus
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    
    # (Kita tetap simpan ini sebagai 'snapshot' harga saat itu)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

# ==================================
#  ▼▼▼ 3. BUAT MODEL RATING BARU ▼▼▼
# ==================================
class Rating(models.Model):
    # Kita hubungkan rating ke 'OrderItem'
    # Satu OrderItem hanya bisa punya satu rating
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating}/5 untuk {self.product.name} oleh {self.user.username}"
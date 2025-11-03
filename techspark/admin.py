from django.contrib import admin
from .models import Product, Address, OrderItem, Rating

admin.site.register(Product)
admin.site.register(Address)
admin.site.register(OrderItem)
admin.site.register(Rating)
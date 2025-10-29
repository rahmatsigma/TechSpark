from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'), 
    
    path('beranda/', views.home_view, name='home'),
    
    path('register/', views.register_view, name='register'),

    path('products/', views.product_list_view, name='product_list'),
]
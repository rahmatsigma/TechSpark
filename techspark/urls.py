from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'), 
    
    path('beranda/', views.home_view, name='home'),
    
    path('register/', views.register_view, name='register'),

    path('logout/', views.logout_view, name='logout'),

    path('products/', views.product_list_view, name='product_list'),

    path('pengaturan/', views.settings_view, name='settings'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),

    path('keranjang/', views.cart_detail_view, name='cart_detail'),

    path('keranjang/update/<int:item_id>/', views.update_cart_quantity_view, name='update_cart_quantity'),
    
    path('keranjang/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),

    # === URL DASHBOARD ADMIN KUSTOM (BARU) ===
    # 'R'ead (List)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # 'C'reate
    path('dashboard/product/add/', views.product_add_view, name='product_add'),
    # 'U'pdate
    path('dashboard/product/edit/<int:pk>/', views.product_edit_view, name='product_edit'),
    # 'D'elete
    path('dashboard/product/delete/<int:pk>/', views.product_delete_view, name='product_delete'),
]
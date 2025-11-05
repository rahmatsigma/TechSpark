from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'), 
    path('beranda/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.product_list_view, name='product_list'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('pengaturan/', views.settings_view, name='settings'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('keranjang/', views.cart_detail_view, name='cart_detail'),
    path('keranjang/update/<int:item_id>/', views.update_cart_quantity_view, name='update_cart_quantity'),
    path('keranjang/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'),


    # === URL DASHBOARD ADMIN KUSTOM (BARU) ===
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/product/add/', views.product_add_view, name='product_add'),
    path('dashboard/product/edit/<int:pk>/', views.product_edit_view, name='product_edit'),
    path('dashboard/product/delete/<int:pk>/', views.product_delete_view, name='product_delete'),

    # ================================Dashboard Kategori (BARU)===============================
    path('dashboard/categories/', views.category_list_view, name='category_list'),
    path('dashboard/category/add/', views.category_add_view, name='category_add'),
    path('dashboard/category/edit/<int:pk>/', views.category_edit_view, name='category_edit'),
    path('dashboard/category/delete/<int:pk>/', views.category_delete_view, name='category_delete'),
    path('dashboard/orders/', views.order_list_view, name='order_list'),
    path('dashboard/order/edit/<int:pk>/', views.order_update_view, name='order_update'),

    path('pesananku/', views.order_history_view, name='order_history'),
    path('rate-item/<int:item_id>/', views.rate_item_view, name='rate_item'),
]
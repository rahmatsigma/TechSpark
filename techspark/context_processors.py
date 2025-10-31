from .models import Cart

def cart_context(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        try:
            # Ambil keranjang milik user
            cart = Cart.objects.get(user=request.user)
            # Hitung total 'quantity' (jumlah) dari semua item
            cart_item_count = sum(item.quantity for item in cart.items.all())
        except Cart.DoesNotExist:
            cart_item_count = 0
            
    return {'cart_item_count': cart_item_count}
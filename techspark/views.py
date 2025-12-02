from django.contrib.auth import update_session_auth_hash
from .forms import UserUpdateForm, CustomPasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.db.models import Q
from .models import Product, Cart, CartItem
from .models import Product
from .forms import ProductForm
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from .models import Product, Category, Cart, CartItem, Address, Order, OrderItem, Rating
from .forms import AddressForm, RatingForm, OrderForm
from .models import Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required

def is_staff(user):
    return user.is_staff

# View beranda 
def home_view(request):
    latest_products = Product.objects.all().order_by('-created_at')[:5]
    main_categories = Category.objects.all()[:4]    
    context = {
        'products': latest_products,
        'categories': main_categories, 
    }
    return render(request, 'pages/beranda.html', context)

def about_view(request):
    """
    View untuk halaman About Us
    """
    return render(request, 'pages/about.html')

# === FUNGSI LOGIN  ===
def login_view(request):
    if request.method == 'POST':
        # Ambil data dari form
        login_input = request.POST.get('login_field') 
        password = request.POST.get('password')

        # 1. Cek kredensial pakai 'authenticate'
        user = authenticate(request, username=login_input, password=password)

        # 2. Cek hasilnya
        if user is not None:
            login(request, user) 
            
            # ===== LOGIKA REDIRECT =====
            # Cek apakah user adalah admin/staff
            if user.is_staff:
                messages.success(request, f'Selamat datang, Admin {user.first_name or user.username}!')
                return redirect('dashboard')
            else:
                messages.success(request, f'Selamat datang kembali, {user.first_name}!')
                return redirect('home')
            
        else:
            messages.error(request, 'Email atau password yang Anda masukkan salah.')
            return render(request, 'pages/login.html')  
        
    return render(request, 'pages/login.html')

# === FUNGSI REGISTER  ===
def register_view(request):
    if request.method == 'POST':
        nama_lengkap = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # --- VALIDASI ---
        if password != password_confirm:
            messages.error(request, 'Password dan Konfirmasi Password tidak cocok!')
            return render(request, 'pages/register.html')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email ini sudah terdaftar. Silakan gunakan email lain.')
            return render(request, 'pages/register.html')

        # --- JIKA LOLOS VALIDASI ---
        try:
            # Buat user baru di database
            user = User.objects.create_user(
                username=email,         
                email=email,
                password=password,       
                first_name=nama_lengkap  
            )

            messages.success(request, 'Akun Anda berhasil dibuat! Silakan login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {e}')
            return render(request, 'pages/register.html')

    return render(request, 'pages/register.html')


def product_list_view(request):
    products = Product.objects.all()
    selected_category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    
    selected_category = None
    if selected_category_id:
        products = products.filter(category__id=selected_category_id)
        try:
            selected_category = Category.objects.get(id=selected_category_id)
        except Category.DoesNotExist:
            pass

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    categories = Category.objects.all()
    products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }
        # HTMX
    if request.headers.get('HX-Request'):
        return render(request, 'partials/product_grid.html', context)
    
    return render(request, 'pages/product_list.html', context)

# === VIEWS DASHBOARD ADMIN ===

@login_required(login_url='login')
@user_passes_test(is_staff)
def dashboard_view(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'pages/dashboard.html', {'products': products})

@login_required(login_url='login')
@user_passes_test(is_staff)
def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Produk baru berhasil ditambahkan!')
            return redirect('dashboard')
    else:
        form = ProductForm()
        
    return render(request, 'pages/product_form.html', {'form': form, 'title': 'Tambah Produk Baru'})

@login_required(login_url='login')
@user_passes_test(is_staff)
def product_edit_view(request, pk):
    # 'U'pdate - Edit produk
    product = get_object_or_404(Product, pk=pk) # Ambil produk berdasarkan ID (pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diperbarui!')
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'pages/product_form.html', {'form': form, 'title': f'Edit Produk: {product.name}'})

@login_required(login_url='login')
@user_passes_test(is_staff)
def product_delete_view(request, pk):
    # 'D'elete - Hapus produk
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produk berhasil dihapus.')
        return redirect('dashboard')
        
    return render(request, 'pages/product_confirm_delete.html', {'product': product})

@login_required(login_url='login')
def buy_now_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Simpan data beli langsung ke session (bukan ke keranjang)
    request.session['buy_now'] = {
        'product_id': product.id,
        'product_name': product.name,
        'product_price': float(product.price),  # Konversi Decimal ke float
        'product_image': product.image_url,
        'quantity': 1
    }
    
    return redirect('checkout')

@login_required 
def logout_view(request):
    logout(request)
    messages.success(request, "Anda berhasil logout.")
    return redirect('login')

# === TAMBAHKAN VIEW BARU INI ===
@login_required(login_url='login') # Pastikan user sudah login
def settings_view(request):
    
    if request.method == 'POST':
        # Cek form mana yang di-submit
        if 'update_info_submit' in request.POST:
            # === Ini logika untuk Form Ganti Nama ===
            user_form = UserUpdateForm(request.POST, instance=request.user)
            password_form = CustomPasswordChangeForm(user=request.user) # Buat form kosong
            
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Nama Anda berhasil diperbarui!')
                return redirect('settings')
        
        elif 'change_password_submit' in request.POST:
            # === Ini logika untuk Form Ganti Password ===
            user_form = UserUpdateForm(instance=request.user) # Buat form kosong
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            
            if password_form.is_valid():
                user = password_form.save()
                # PENTING: Update sesi agar user tidak auto-logout
                update_session_auth_hash(request, user) 
                messages.success(request, 'Password Anda berhasil diubah!')
                return redirect('settings')
    
    else:
        # === Ini logika untuk GET (user baru buka halaman) ===
        user_form = UserUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    # Kirim kedua form ke template
    context = {
        'user_form': user_form,
        'password_form': password_form
    }
    return render(request, 'pages/settings.html', context)


@login_required(login_url='login') 
def add_to_cart_view(request, product_id):
    # 1. Ambil produk yang mau ditambahkan
    product = get_object_or_404(Product, id=product_id)
    
    # 2. Ambil keranjang milik user 
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # 3. Cek apakah produk sudah ada di keranjang
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        # Jika sudah ada, tambah jumlahnya (quantity)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Jumlah '{product.name}' di keranjang diperbarui.")
    else:
        # Jika baru, biarkan quantity = 1 (default)
        messages.success(request, f"'{product.name}' berhasil ditambahkan ke keranjang.")

    # 4. Arahkan user kembali ke halaman sebelumnya
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def cart_detail_view(request):
    # Ambil keranjang user (atau buat jika belum ada)
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all().order_by('product__name')
    
    # Hitung total harga
    total_price = sum(item.subtotal for item in items)
    
    context = {
        'items': items,
        'total_price': total_price
    }
    return render(request, 'pages/cart_detail.html', context)


@login_required(login_url='login')
def update_cart_quantity_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity > 0:
                if quantity <= item.product.stock:
                    item.quantity = quantity
                    item.save()
                    messages.success(request, f"Jumlah '{item.product.name}' diperbarui.")
                else:
                    messages.error(request, f"Stok '{item.product.name}' tidak mencukupi (tersisa {item.product.stock}).")
            else:
                # Jika user set ke 0 atau kurang, hapus saja
                item.delete()
                messages.success(request, f"'{item.product.name}' dihapus dari keranjang.")
        except ValueError:
            messages.error(request, "Jumlah tidak valid.")
            
    return redirect('cart_detail')


@login_required(login_url='login')
def remove_from_cart_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item_name = item.product.name
    item.delete()
    messages.success(request, f"'{item_name}' telah dihapus dari keranjang.")
    return redirect('cart_detail')


@login_required(login_url='login')
@user_passes_test(is_staff)
def category_list_view(request):
    # 'R'ead - Tampilkan semua kategori
    categories = Category.objects.all().order_by('name')
    return render(request, 'pages/category_list.html', {'categories': categories})

@login_required(login_url='login')
@user_passes_test(is_staff)
def category_add_view(request):
    # 'C'reate - Tambah kategori baru
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori baru berhasil ditambahkan!')
            return redirect('category_list')
    else:
        form = CategoryForm()
        
    return render(request, 'pages/category_form.html', {'form': form, 'title': 'Tambah Kategori Baru'})

@login_required(login_url='login')
@user_passes_test(is_staff)
def category_edit_view(request, pk):
    # 'U'pdate - Edit kategori
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori berhasil diperbarui!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
        
    return render(request, 'pages/category_form.html', {'form': form, 'title': f'Edit Kategori: {category.name}'})

@login_required(login_url='login')
@user_passes_test(is_staff)
def category_delete_view(request, pk):
    # 'D'elete - Hapus kategori
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, 'Kategori berhasil dihapus.')
        except:
            messages.error(request, 'Kategori ini tidak bisa dihapus karena masih digunakan oleh produk.')
        return redirect('category_list')
        
    return render(request, 'pages/category_confirm_delete.html', {'category': category})


@login_required(login_url='login')
@user_passes_test(is_staff)
def order_list_view(request):
    # 'R'ead - Tampilkan semua pesanan, yang terbaru di atas
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'pages/order_list.html', {'orders': orders})

@login_required(login_url='login')
@user_passes_test(is_staff)
def order_update_view(request, pk):
    # 'U'pdate - Edit status pesanan
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Status untuk Pesanan #{order.id} berhasil diperbarui.")
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
        
    context = {
        'form': form,
        'order': order
    }
    return render(request, 'pages/order_update.html', context)


# ==================================
#  ▼▼▼ VIEW CHECKOUT & SUCCESS ▼▼▼
# ==================================

@login_required(login_url='login')
def checkout_view(request):
    # CEK APAKAH INI DARI "BELI LANGSUNG" ATAU KERANJANG NORMAL
    buy_now_data = request.session.get('buy_now')
    
    if buy_now_data:
        # === FLOW BELI LANGSUNG ===
        product = get_object_or_404(Product, id=buy_now_data['product_id'])
        items = [{
            'product': product,
            'quantity': buy_now_data['quantity'],
            'subtotal': product.price * buy_now_data['quantity']
        }]
        total_price = float(product.price) * buy_now_data['quantity']
        is_buy_now = True
        cart = None
    else:
        # === FLOW KERANJANG NORMAL ===
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            messages.error(request, "Keranjang Anda kosong.")
            return redirect('home')

        items = list(cart.items.all())  # CONVERT KE LIST
        total_price = sum(item.subtotal for item in items)
        is_buy_now = False

        if len(items) == 0:
            messages.error(request, "Anda tidak bisa checkout dengan keranjang kosong.")
            return redirect('cart_detail')

    try:
        default_address = Address.objects.get(user=request.user, is_default=True)
        form = AddressForm(instance=default_address)
    except Address.DoesNotExist:
        form = AddressForm()

    if request.method == 'POST':
        form = AddressForm(request.POST)
        
        if form.is_valid():
            payment_method = request.POST.get('payment_method')

            address = form.save(commit=False)
            address.user = request.user
            address.save()
            
            if not Address.objects.filter(user=request.user, is_default=True).exists():
                address.is_default = True
                address.save()

            order = Order.objects.create(
                user=request.user,
                full_name=address.full_name,
                phone=address.phone,
                shipping_address=f"{address.street_address}, {address.city}, {address.province}, {address.postal_code}",
                total_price=total_price,
                payment_method=payment_method
            )

            if is_buy_now:
                # === CREATE ORDER ITEM DARI BUY_NOW ===
                product = get_object_or_404(Product, id=buy_now_data['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    product_price=product.price,
                    quantity=buy_now_data['quantity']
                )
                product.stock -= buy_now_data['quantity']
                product.save()
                # Hapus data buy_now dari session
                del request.session['buy_now']
            else:
                # === CREATE ORDER ITEM DARI KERANJANG ===
                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        product_price=item.product.price,
                        quantity=item.quantity
                    )
                    
                    item.product.stock -= item.quantity
                    item.product.save()
                
                cart.items.all().delete()
            
            messages.success(request, "Pesanan Anda berhasil dibuat!")
            return redirect('order_success', order_id=order.id)

    context = {
        'items': items,
        'total_price': total_price,
        'form': form,
        'is_buy_now': is_buy_now
    }
    return render(request, 'pages/checkout.html', context)


@login_required(login_url='login')
def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order
    }
    # Halaman "Terima Kasih"
    return render(request, 'pages/order_success.html', context)


@login_required(login_url='login')
def order_history_view(request):
    # Ambil semua pesanan user, prefetch item & ratingnya
    orders = Order.objects.filter(user=request.user).prefetch_related(
        'items', 
        'items__product', 
        'items__rating' # Ambil rating terkait (jika ada)
    ).order_by('-created_at')
    
    return render(request, 'pages/order_history.html', {'orders': orders})


@login_required(login_url='login')
def rate_item_view(request, item_id):
    # Ambil item, pastikan itu milik user
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)

    # Cek 1: Hanya bisa rating jika order 'Selesai'
    if item.order.status != 'completed':
        messages.error(request, 'Anda hanya bisa memberi rating pada pesanan yang sudah selesai.')
        return redirect('order_history')
    
    # Cek 2: Cek apakah sudah pernah dirating
    if hasattr(item, 'rating'): # (Cek one-to-one field 'rating')
        messages.error(request, 'Anda sudah memberi rating untuk produk ini.')
        return redirect('order_history')

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.order_item = item       # Tautkan ke OrderItem
            rating.user = request.user     # Tautkan ke User
            rating.product = item.product  # Tautkan ke Product
            rating.save()
            messages.success(request, 'Rating Anda berhasil disimpan!')
            return redirect('order_history')
    else:
        form = RatingForm()

    context = {
        'form': form,
        'item': item
    }
    return render(request, 'pages/rate_item.html', context)


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    reviews = Rating.objects.filter(product=product).order_by('-created_at')
    
    avg_rating_data = reviews.aggregate(Avg('rating'))
    avg_rating = avg_rating_data['rating__avg'] or 0.0
    review_count = reviews.count()

    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count
    }
    return render(request, 'pages/product_detail.html', context)
from django.contrib.auth import update_session_auth_hash
from .forms import UserUpdateForm, CustomPasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

def is_staff(user):
    return user.is_staff

# View beranda 
def home_view(request):
    return render(request, 'pages/beranda.html') 

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

# View list produk 
def product_list_view(request):
    products = Product.objects.all().order_by('-created_at') 
    
    context = {
        'products': products
    }
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
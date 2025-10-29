from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

# View beranda (tidak berubah)
def home_view(request):
    return render(request, 'pages/beranda.html') 

# === FUNGSI LOGIN (VERSI LENGKAP) ===
def login_view(request):
    if request.method == 'POST':
        # Ambil data dari form
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 1. Cek kredensial pakai 'authenticate'
        # Kita pakai 'email' sebagai 'username'
        user = authenticate(request, username=email, password=password)

        # 2. Cek hasilnya
        if user is not None:
            # Jika user ada dan password-nya benar
            login(request, user)  # Buat sesi login untuk user
            
            # (Opsional) Kasih pesan selamat datang
            messages.success(request, f'Selamat datang kembali, {user.first_name}!')
            
            # Arahkan ke halaman beranda
            return redirect('home')
        else:
            # Jika user tidak ada atau password salah
            messages.error(request, 'Email atau password yang Anda masukkan salah.')
            # Kembalikan ke halaman login (untuk menampilkan pesan error)
            return render(request, 'pages/login.html')

    # Jika metodenya GET (baru buka halaman), tampilkan halaman login
    return render(request, 'pages/login.html')

# === FUNGSI REGISTER (VERSI LENGKAP) ===
def register_view(request):
    if request.method == 'POST':
        # Ambil semua data dari form register
        nama_lengkap = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # --- VALIDASI ---
        # 1. Cek apakah password & konfirmasi sama
        if password != password_confirm:
            messages.error(request, 'Password dan Konfirmasi Password tidak cocok!')
            return render(request, 'pages/register.html')
        
        # 2. Cek apakah email (username) sudah terdaftar
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email ini sudah terdaftar. Silakan gunakan email lain.')
            return render(request, 'pages/register.html')

        # --- JIKA LOLOS VALIDASI ---
        try:
            # 3. Buat user baru di database
            user = User.objects.create_user(
                username=email,          # Kita pakai email sebagai username
                email=email,
                password=password,       # Django akan HASH password ini
                first_name=nama_lengkap  # Menyimpan nama lengkap
            )
            # user.save() tidak perlu, create_user sudah otomatis menyimpan

            # 4. Beri pesan sukses dan arahkan ke login
            messages.success(request, 'Akun Anda berhasil dibuat! Silakan login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {e}')
            return render(request, 'pages/register.html')

    # Jika metodenya GET, tampilkan halaman register
    return render(request, 'pages/register.html')

# View list produk (tidak berubah)
def product_list_view(request):
    return render(request, 'pages/product_list.html')
from django import forms
from .models import Product, Category, Address
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Product

# 1. Form CRUD Produk (Sudah ada)
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image_url', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})

        }
        labels = {
            'name': 'Nama Produk',
            'description': 'Deskripsi',
            'price': 'Harga (Rupiah)',
            'image_url': 'URL Gambar Produk',
            'stock': 'Stok Produk',
            'category': 'Kategori Produk',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name'] # Hanya field 'name'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nama Kategori',
        }

# 2. Form untuk ganti Nama
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['first_name'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nama lengkap Anda'})
        self.fields['first_name'].label = "Nama Lengkap"

# 3. Form untuk ganti Password
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Masukkan password lama'})
        self.fields['old_password'].label = "Password Lama"
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Masukkan password baru'})
        self.fields['new_password1'].label = "Password Baru"
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Konfirmasi password baru'})
        self.fields['new_password2'].label = "Konfirmasi Password Baru"


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        # Kita tidak perlu 'user' dan 'is_default' di form
        fields = ['full_name', 'phone', 'street_address', 'city', 'province', 'postal_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tambahkan style & label Bahasa Indonesia
        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nama Lengkap Penerima'})
        self.fields['full_name'].label = "Nama Lengkap"
        
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': '0812xxxx'})
        self.fields['phone'].label = "Nomor Telepon"
        
        self.fields['street_address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nama jalan, nomor rumah, RT/RW'})
        self.fields['street_address'].label = "Alamat Jalan"
        
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contoh: Kota Madiun'})
        self.fields['city'].label = "Kota / Kabupaten"
        
        self.fields['province'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contoh: Jawa Timur'})
        self.fields['province'].label = "Provinsi"
        
        self.fields['postal_code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contoh: 63112'})
        self.fields['postal_code'].label = "Kode Pos"
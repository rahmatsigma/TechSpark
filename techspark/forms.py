from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm # Impor form bawaan Django
from .models import Product

# 1. Form CRUD Produk (Sudah ada)
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nama Produk',
            'description': 'Deskripsi',
            'price': 'Harga (Rupiah)',
            'image_url': 'URL Gambar Produk',
            'stock': 'Stok Produk',
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
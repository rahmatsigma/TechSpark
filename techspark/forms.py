from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Tampilkan semua field dari model Product di form
        fields = ['name', 'description', 'price', 'image_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nama Produk',
            'description': 'Deskripsi',
            'price': 'Harga (Rupiah)',
            'image_url': 'URL Gambar Produk'
        }
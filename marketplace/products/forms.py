from django import forms

from .models import Product


class CreateProductForm(forms.ModelForm):
    image = forms.ImageField(required=True, label="Загрузите аватар", widget=forms.FileInput(attrs={'class': 'image-input'}))

    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price']

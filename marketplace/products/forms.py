from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Product, Category, Comment


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class CreateProductForm(forms.ModelForm):
    images = MultipleFileField()
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория")

    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


class CreateCommentForm(forms.ModelForm):
    rate = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        label='Оценка',
        required=True,
        widget=forms.Select(attrs={'class': 'form-input'})  # Добавляем класс для Select
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input'}),  # Добавляем класс для Textarea
        label='Комментарий',
        required=False
    )

    class Meta:
        model = Comment
        fields = ['rate', 'text']


class UpdateProductForm(forms.ModelForm):
    images = MultipleFileField(label="Добавь новые фотографии", required=False)

    name = forms.CharField(label="Название")
    description = forms.CharField(label="Описание", widget=forms.Textarea)
    price = forms.IntegerField(label="Цена")
    total_price = forms.IntegerField(label="Итоговая цена",
                                     widget=forms.NumberInput(attrs={'readonly': 'readonly'}),
                                     required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория")
    discount = forms.IntegerField(
        label="Скидка (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        widget=forms.NumberInput(attrs={'min': 0, 'max': 100})
    )
    is_available = forms.BooleanField(label="Если ли в наличии")

    class Meta:
        model = Product
        fields = ['name', 'description',
                  'price', 'category',
                  'total_price', 'discount', 'is_available']

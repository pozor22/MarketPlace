from django import forms

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
    rate = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], label='Оценка', required=True)
    text = forms.CharField(widget=forms.Textarea, label='Комментарий', required=False)

    class Meta:
        model = Comment
        fields = ['rate', 'text']

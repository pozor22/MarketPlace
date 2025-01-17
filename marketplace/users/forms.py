from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class CreateUserForm(UserCreationForm):
    image = forms.ImageField(required=False, label="Загрузите аватар", widget=forms.FileInput(attrs={'class': 'image-input'}))

    class Meta:
        model = User
        fields = ['image', 'username', 'email', 'password1', 'password2']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_new_password = forms.CharField(label='Подтвердите новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        # Получаем объект пользователя из аргументов
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        # Проверяем, введен ли правильный текущий пароль
        old_password = self.cleaned_data.get('old_password')
        if self.user and not self.user.check_password(old_password):
            raise forms.ValidationError('Старый пароль введен неверно')
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise forms.ValidationError('Пароли не совпадают')
        if old_password == new_password:
            raise forms.ValidationError('Новый пароль не должен совпадать со старым')
        return cleaned_data


class ConfirmPasswordChangeForm(forms.Form):
    code = forms.CharField(label="Код подтверждения", widget=forms.TextInput(attrs={'class': 'form-control'}))

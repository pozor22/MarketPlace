from django.contrib.auth.forms import UserCreationForm
from django import forms
import re

from .models import User


class CreateUserForm(UserCreationForm):
    image = forms.ImageField(required=False, label="Загрузите аватар", widget=forms.FileInput(attrs={'class': 'image-input'}))

    class Meta:
        model = User
        fields = ['image', 'username', 'email', 'password1', 'password2']


class UpdateToSellerUserForm(forms.Form):
    inn = forms.CharField(
        label="ИНН",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Введите ИНН', 'class': 'form-control'}),
        help_text="ИНН должен содержать ровно 12 цифр."
    )
    address = forms.CharField(
        label="Адрес проживания",
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Введите адрес', 'rows': 3, 'class': 'form-control'}),
        help_text="Введите полный адрес проживания."
    )
    phone_number = forms.CharField(
        label="Номер телефона",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона', 'class': 'form-control phone-input', 'type': 'tel', 'pattern': r'^(8|\+7)\d{10,15}'}),
        help_text="Введите номер телефона в формате: +7 или 8-XXX-XXX-XXXX."
    )

    def clean_inn(self):
        inn = self.cleaned_data.get('inn')
        if not inn.isdigit():
            raise forms.ValidationError("ИНН должен содержать только цифры.")
        if len(inn) != 12:
            raise forms.ValidationError("ИНН должен содержать ровно 12 цифр.")
        return inn

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Проверяем, соответствует ли номер телефона формату XXX-XXX-XXXX
        if not re.match(r'^(8|\+7)\d{10,15}', phone_number):
            raise forms.ValidationError("Введите номер телефона в формате: +7 или 8-XXX-XXX-XXXX.")
        return phone_number


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

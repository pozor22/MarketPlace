from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
import base64
import random


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    avatar = models.BinaryField(null=True, blank=True)

    # Данные для продавца
    inn = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{12}$',
                message='ИНН должен содержать ровно 12 цифр.',
                code='invalid_inn'
            )
        ],
        verbose_name="ИНН"
    )
    address = models.TextField(null=True, blank=True, verbose_name="Адрес проживания")
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message='Номер телефона должен содержать от 10 до 15 цифр, с опциональным "+" в начале.',
                code='invalid_phone_number'
            )
        ],
        verbose_name="Номер телефона"
    )

    def get_image_base64(self):
        """Возвращает изображение в формате base64 для использования в шаблоне"""
        if self.avatar:
            return base64.b64encode(self.avatar).decode('utf-8')
        return None

    def save(self, *args, **kwargs):
        # Если поле `image` пустое, использовать дефолтное изображение
        if not self.avatar:
            default_image_path = 'users/media/users/images/default_avatar_user.png'
            try:
                with open(default_image_path, 'rb') as f:
                    self.avatar = f.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"Дефолтное изображение не найдено по пути: {default_image_path}")

        super().save(*args, **kwargs)


class PasswordChangeConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="password_change_confirmation")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_confirmation_code(self):
        self.code = f'{random.randint(100000, 999999)}'
        self.save()

    def is_code_valid(self):
        from datetime import timedelta
        from django.utils.timezone import now
        return now() - self.created_at <= timedelta(minutes=10)

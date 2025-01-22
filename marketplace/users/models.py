import base64
import random
from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    avatar = models.BinaryField(null=True, blank=True)

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

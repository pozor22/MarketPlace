from django.contrib.auth.models import AbstractUser
from django.db import models
import base64


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

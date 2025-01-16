from django.db import models
import base64


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.BinaryField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='products')

    def get_image_base64(self):
        """Возвращает изображение в формате base64 для использования в шаблоне"""
        if self.image:
            return base64.b64encode(self.image).decode('utf-8')
        return None

    def save(self, *args, **kwargs):
        # Если поле `image` пустое, использовать дефолтное изображение
        if not self.image:
            default_image_path = 'products/media/products/images/default_avatar_product.png'
            try:
                with open(default_image_path, 'rb') as f:
                    self.image = f.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"Дефолтное изображение не найдено по пути: {default_image_path}")

        super().save(*args, **kwargs)  # Сохранение объекта

    def __str__(self):
        return self.name

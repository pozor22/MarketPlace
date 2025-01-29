from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import base64


class Like(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} liked {self.product.name}"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Название категории
    description = models.TextField(blank=True, null=True)  # Описание категории (необязательно)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=False, default=1)
    total_price = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=False, default=1)
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products', default=1)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.discount > 0:
            self.total_price = self.price - (self.price * self.discount / 100)
        else:
            self.total_price = self.price

        super().save(*args, **kwargs)  # Сохранение объекта

    def get_ratings(self):
        return self.comments.aggregate(models.Avg('rate'))['rate__avg']

    def get_comments_count(self):
        return self.comments.count()

    def get_likes_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'product')

    def __str__(self):
        return f"Comment for {self.product.name} and rate {self.rate}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.BinaryField()  # Хранение изображения в бинарном формате
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Конвертируем изображение в бинарный формат, если оно в виде пути
        if isinstance(self.image, str):  # Если путь к файлу
            with open(self.image, 'rb') as f:
                self.image = f.read()
        super().save(*args, **kwargs)  # Сохранение объекта

    def get_image_base64(self):
        """Возвращает изображение в формате base64 для использования в шаблоне"""
        return base64.b64encode(self.image).decode('utf-8')

    def __str__(self):
        return f"Image for {self.product.name}"

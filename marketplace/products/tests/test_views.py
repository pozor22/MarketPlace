from django.test import TestCase
from django.urls import reverse

from products.models import Product, Category, Like
from users.models import User, Basket


class HomeProductsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='test')

        category = Category.objects.create(name='Category 1')

        for i in range(30):
            Product.objects.create(name=f"Procuts {i}",
                                   description=f'Description {i}',
                                   price=111,
                                   author=cls.user,
                                   category=category)

    def test_home_products_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/home.html')
        self.assertIn('products', response.context)
        self.assertEqual(len(response.context['products']), 20)

    def test_pagination_home_products_list_view(self):
        response = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/home.html')
        self.assertIn('products', response.context)
        self.assertEqual(len(response.context['products']), 10)

    def test_post_add_to_basket(self):
        self.client.login(username='test', password='test')

        product = Product.objects.first()
        response = self.client.post(reverse('home'), {'add_to_basket': product.id})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Basket.objects.filter(user=self.user, product=product).exists())

    def test_add_to_basket_not_authenticated(self):
        product = Product.objects.first()
        response = self.client.post(reverse('home'), {'add_to_basket': product.id})

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Basket.objects.filter(user=self.user, product=product).exists())
        self.assertRedirects(response, reverse('login'))

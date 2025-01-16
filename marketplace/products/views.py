from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


class HomeProducts(ListView):
    template_name = 'products/home.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/DetailProduct.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

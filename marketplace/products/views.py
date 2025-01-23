from django.db.transaction import commit
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import Product, ProductImage
from .forms import CreateProductForm


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


class CreateProductView(CreateView):
    model = Product
    template_name = 'products/create_product.html'
    form_class = CreateProductForm

    def form_valid(self, form):
        product = form.save(commit=False)
        product.author = self.request.user
        product.save()

        images = self.request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(
                product=product,
                image=image.read()  # Сохраняем содержимое файла в бинарном формате
            )

        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create product'
        return context

from django.shortcuts import render
from django.views.generic import ListView
from .models import Product


class Home_Products(ListView):
    template_name = 'products/home.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context

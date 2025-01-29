from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView
from django.utils.timezone import localtime

from .models import Product, ProductImage
from .forms import CreateProductForm, CreateCommentForm


class HomeProducts(ListView):
    template_name = 'products/home.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()

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

        form_comment = CreateCommentForm()

        comments = self.object.comments.all().order_by('-created_at')
        for comment in comments:
            comment.formatted_date = localtime(comment.created_at).strftime("%d.%m.%Y %H:%M")

        context['title'] = self.object.name
        context['form_comment'] = form_comment
        context['comments'] = comments
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        product = self.get_object()
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.author = request.user
            comment.save()
            return redirect('product_detail', pk=product.pk)

        return self.get(request, *args, **kwargs)


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

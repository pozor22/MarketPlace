from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from .models import Product, ProductImage, Like, Comment
from .forms import CreateProductForm, CreateCommentForm, UpdateProductForm
from .mixins import SellerRequiredMixin, NotAuthenticatedRequiredMixin
from users.models import Basket


class HomeProducts(ListView):
    template_name = 'products/home.html'
    context_object_name = 'products'
    paginate_by = 20

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        if "add_to_basket" in request.POST:
            product_id = request.POST.get('add_to_basket')
            product = Product.objects.get(id=product_id)
            Basket.objects.get_or_create(user=request.user, product=product)
            return self.get(request)

    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class ProductsUserLiked(NotAuthenticatedRequiredMixin, ListView):
    template_name = 'products/products_liked.html'
    context_object_name = 'products'
    paginate_by = 20

    def post(self, request):
        if "add_to_basket" in request.POST:
            product_id = request.POST.get('add_to_basket')
            product = Product.objects.get(id=product_id)
            Basket.objects.get_or_create(user=request.user, product=product)
            return self.get(request)

    def get_queryset(self):
        return Product.objects.prefetch_related('images').filter(likes__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MyLiked'
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/detail_product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form_comment = CreateCommentForm()

        comments = self.object.comments.all().order_by('-created_at')

        for comment in comments:
            comment.formatted_date = localtime(comment.created_at).strftime("%d.%m.%Y %H:%M")

        is_comment = self.object.comments.filter(author=self.request.user).exists() if self.request.user.is_authenticated else False
        if is_comment:
            context['comment'] = self.object.comments.get(author=self.request.user, product=self.get_object())
            form_comment = CreateCommentForm(initial={'text': context['comment'].text})

        context['title'] = self.object.name
        context['form_comment'] = form_comment
        context['comments'] = comments
        context['is_comment'] = is_comment
        context['is_liked'] = self.object.is_liked_by(self.request.user) if self.request.user.is_authenticated else False
        context['likes_count'] = self.object.likes.count()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if "like" in request.POST:
            return self.like_product(request)

        if "delete" in request.POST:
            try:
                comment = Comment.objects.get(author=request.user, product=self.get_object())
                comment.delete()
            except Comment.DoesNotExist:
                pass

            return self.get(request, *args, **kwargs)

        if "add_to_basket" in request.POST:
            product_id = request.POST.get('add_to_basket')
            product = Product.objects.get(id=product_id)
            Basket.objects.get_or_create(user=request.user, product=product)
            return self.get(request, *args, **kwargs)

        product = self.get_object()
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            # Проверяем, существует ли уже комментарий от текущего пользователя
            user_comment = product.comments.filter(author=request.user, product=self.get_object()).first()

            if user_comment:
                # Если комментарий уже существует, обновляем его
                user_comment.rate = request.POST.get('rate')
                user_comment.text = form.cleaned_data['text']
                user_comment.save()
            else:
                # Если комментария нет, создаем новый
                comment = form.save(commit=False)
                comment.product = product
                comment.author = request.user
                comment.rate = request.POST.get('rate')
                comment.save()

            return redirect('product_detail', pk=product.pk)

        return self.get(request, *args, **kwargs)

    def like_product(self, request):
        product = self.get_object()
        like, created = Like.objects.get_or_create(product=product, user=request.user)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({
            "liked": liked,
            "likes_count": product.likes.count()
        })


class ProfileSeller(SellerRequiredMixin, ListView):
    template_name = 'products/profile_seller.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.prefetch_related('images').filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ProfileSeller'
        return context


class ProductDetailSeller(SellerRequiredMixin, DetailView):
    template_name = 'products/detail_product_seller.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = UpdateProductForm(initial={
            'name': self.object.name,
            'description': self.object.description,
            'price': self.object.price,
            'category': self.object.category,
            'total_price': self.object.total_price,
            'discount': self.object.discount,
            'is_available': self.object.is_available
        })

        context['title'] = 'Товар'
        context['form'] = form
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if "delete_image" in request.POST:
            image_id = request.POST.get('delete_image')
            image = ProductImage.objects.get(id=image_id)
            image.delete()
            return self.get(request)

        if "delete_product" in request.POST:
            product = self.get_object()
            product.delete()
            return redirect('profile_seller')

        form = UpdateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = self.get_object()
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.price = form.cleaned_data['price']
            product.category = form.cleaned_data['category']
            product.discount = form.cleaned_data['discount']
            product.is_available = form.cleaned_data['is_available']
            product.save()

            images = request.FILES.getlist('images')
            for image in images:
                 ProductImage.objects.create(
                    product=product,
                    image=image.read()
                )

            return self.get(request)

        return self.get(request)


class CreateProductView(SellerRequiredMixin, CreateView):
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

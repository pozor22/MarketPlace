from django.urls import path
from . import views


urlpatterns = [
    path('<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('create/', views.CreateProductView.as_view(), name='create_product'),
]

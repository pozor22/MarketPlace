from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home_Products.as_view(), name='home'),
]

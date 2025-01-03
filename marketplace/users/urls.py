from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CreateUserView, LoginUserView

urlpatterns = [
    path('registration/', CreateUserView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

from django.urls import path
from .views import CreateUserView, LoginUserView

urlpatterns = [
    path('registration/', CreateUserView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
]

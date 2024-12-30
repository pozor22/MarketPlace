from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CreateUserForm


class CreateUserView(CreateView):
    template_name = 'users/registration.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('login')


class LoginUserView(LoginView):
    template_name = 'users/login.html'

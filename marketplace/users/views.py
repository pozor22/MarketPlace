from django.views.generic import CreateView, View, TemplateView
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site

from .forms import CreateUserForm, ChangePasswordForm
from .tasks import send_email_active_account
from .models import User
from .mixins import UserIsNotAuthenticated


class CreateUserView(UserIsNotAuthenticated, CreateView):
    template_name = 'users/registration.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False

        image = self.request.FILES.get('image')
        if image:
            user.avatar = image.read()

        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        send_email_active_account.delay(user.id, domain)
        return redirect('email_confirmation_sent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class LoginUserView(LoginView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class ChangePasswordView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            form = ChangePasswordForm(user=request.user)

            context = {
                'title': 'Изменение пароля',
                'form': form
            }
            return render(request, 'users/change_password.html', context=context)

    def post(selfself, request):
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()

            update_session_auth_hash(request, user)

            return redirect('home')
        else:
            context = {
                'title': 'Изменение пароля',
                'form': form
            }
            return render(request, 'users/change_password.html', context=context)


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context

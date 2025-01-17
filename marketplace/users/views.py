from django.views.generic import CreateView, View, TemplateView
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site

from .forms import CreateUserForm, ChangePasswordForm, ConfirmPasswordChangeForm
from .tasks import send_email_active_account, send_email_code
from .models import User, PasswordChangeConfirmation
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


class LoginUserView(UserIsNotAuthenticated, LoginView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class Profile(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'title': 'Профиль',
            'user': request.user
        }
        return render(request, 'users/profile.html', context=context)


class ChangeUsernameView(LoginRequiredMixin, View):
    def post(self, request):
        new_username = request.POST.get('new_username')
        if new_username:
            if not User.objects.get(username=new_username):
                user = request.user
                user.username = new_username
                user.save()
                messages.success(request, 'Имя пользователя успешно изменено.')
            else:
                messages.error(request, 'Это имя уже занято!!!')
        else:
            messages.error(request, 'Введите имя пользователя!!!')
        return redirect('profile')


class ChangeEmailView(LoginRequiredMixin, View):
    def post(self, request):
        new_email = request.POST.get('new_email')
        if new_email:
            if not User.objects.get(email=new_email):
                user = request.user
                user.email = new_email
                user.save()
                messages.success(request, 'Ваша почта успешно изменена.')
            else:
                messages.error(request, 'Эта почта уже занята!!!')
        else:
            messages.error(request, 'Введите email!!!')
        return redirect('profile')


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangePasswordForm(user=request.user)

        context = {
            'title': 'Изменение пароля',
            'form': form
        }
        return render(request, 'users/change_password.html', context=context)

    def post(self, request):
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            code, _ = PasswordChangeConfirmation.objects.get_or_create(user=user)
            code.generate_confirmation_code()

            send_email_code.delay(user.id, code.code)

            request.session['new_password'] = form.cleaned_data['new_password']
            return redirect('confirm_change_password')

        context = {
            'title': 'Изменение пароля',
            'form': form
        }
        return render(request, 'users/change_password.html', context=context)


class ConfirmPasswordChangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = ConfirmPasswordChangeForm()
        return render(request, 'users/confirm_password_change.html', context={'form': form})

    def post(self, request):
        form = ConfirmPasswordChangeForm(request.POST)
        error_message = None

        if form.is_valid():
            user = request.user
            code = form.cleaned_data["code"]
            try:
                confirmation = PasswordChangeConfirmation.objects.get(user=user)
                if confirmation.code == code and confirmation.is_code_valid():
                    new_password = request.session.pop('new_password', None)
                    if new_password:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)
                        confirmation.delete()
                        return redirect('home')
                    else:
                        error_message = 'Не удалось сменить пароль.'
                else:
                    error_message = 'Неверный код подтверждения или код устарел.'
            except PasswordChangeConfirmation.DoesNotExist:
                error_message = 'Код подтверждения не найден.'

        context = {
            'form': form,
            'error_message': error_message,
            'title': 'Подтверждение смены пароля'
        }

        return render(request, 'users/confirm_password_change.html',context=context)


class ResendCodeView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        code, _ = PasswordChangeConfirmation.objects.get_or_create(user=user)
        code.generate_confirmation_code()

        send_email_code.delay(user.id, code.code)
        return redirect('confirm_change_password')


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

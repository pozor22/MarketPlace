from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),

    path('registration/', views.CreateUserView.as_view(), name='registration'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('/change_username/', views.ChangeUsernameView.as_view(), name='change_username'),
    path('change_email/', views.ChangeEmailView.as_view(), name='change_email'),

    path('change_pass/', views.ChangePasswordView.as_view(), name='change_pass'),
    path('confirm_change_pass/', views.ConfirmPasswordChangeView.as_view(), name='confirm_change_password'),
    path('resend_code/', views.ResendCodeView.as_view(), name='resend_code'),

    path('confirm_email/<str:uidb64>/<str:token>/', views.UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmation_sent/', views.EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('email_confirmed/', views.EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm_email_failed/', views.EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
]

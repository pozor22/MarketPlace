from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('registration/', views.CreateUserView.as_view(), name='registration'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('confirm-email/<str:uidb64>/<str:token>/', views.UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmation_sent/', views.EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('email-confirmed/', views.EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', views.EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
]

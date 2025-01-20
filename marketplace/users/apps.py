from django.apps import AppConfig
from django.core.management import call_command


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    #пока она будет в коммите, потому что сейчас не нужно мне все время проверять, что роли создались(оно работает)
    # def ready(self):
    #     try:
    #         call_command('initialize_roles')
    #     except Exception as e:
    #         print(f"Error initializing roles: {e}")

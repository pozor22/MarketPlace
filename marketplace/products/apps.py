from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    # пока она будет в коммите, потому что сейчас не нужно мне все время проверять, что категории создались(оно работает)
    # def ready(self):
    #     try:
    #         call_command('initialize_categories')
    #     except Exception as e:
    #         print(f"Error initializing categories: {e}")

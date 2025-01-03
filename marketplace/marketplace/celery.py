from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем настройки Django для использования Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')

app = Celery('MarketplaceCelery')

# Загружаем конфигурацию из settings.py, префикс CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в приложениях
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

import os
from celery import Celery
from django.conf import settings

# Установка модуля настроек Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morfix_django_restapi.settings')

# Создание экземпляра Celery
app = Celery('morfix_django_restapi')

# Загрузка настроек Celery из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач из всех установленных приложений
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

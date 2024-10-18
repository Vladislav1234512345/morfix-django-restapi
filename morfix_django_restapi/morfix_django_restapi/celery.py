import os
from celery import Celery

# Установка модуля настроек Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')

# Загрузка настроек Celery из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач из всех приложений
app.autodiscover_tasks()

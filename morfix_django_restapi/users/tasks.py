from django.utils import timezone
from celery import shared_task
from datetime import timedelta

from .models import User

from django.conf import settings

# Задача для всех приложений
@shared_task
# Функция обновелния неактивных пользователей
def update_inactive_users():
    # Дата и время сейчас
    now = timezone.now()
    # Возвращает время ожидания, если в параметре переданы seconds=15, то вернет: 00.00.15
    last_activity_threshold = timedelta(
        seconds=settings.CELERY_BEAT_SCHEDULE.get('mark-inactive-every-minute').get('schedule', 10)
    )
    # Получаем всех пользователей, которые станут неактивными
    inactive_users = User.objects.filter(
        # Поле is_active должно быть True
        is_online=True,
        # Последння активность пользователя < дата и время сейчас - время ожидания
        last_activity__lt=now - last_activity_threshold
    )
    # Обновления неактивных пользователей: is_online поле становиться False
    inactive_users.update(is_online=False)
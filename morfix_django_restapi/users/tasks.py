from celery import shared_task
from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from morfix_django_restapi.settings import redis_client

channel_layer = get_channel_layer()

# Задача для всех приложений
@shared_task
# Функция обновелния неактивных пользователей
def for_active_users_update_other_users_activity():
    active_users_encoded = redis_client.smembers('active_users')

    active_users = {int(user.decode('utf-8')) for user in active_users_encoded}

    for active_user in active_users:
        # Отправка обновления списка чатов
        async_to_sync(channel_layer.group_send)(
            f"user_{active_user}",
            {
                "type": "send.active.users",
            }
        )
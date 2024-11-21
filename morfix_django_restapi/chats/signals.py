# signals.py
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from django.db.models.signals import post_save

from .functions import count_unseen_chats
from .models import Message, ChatEvent

from channels.layers import get_channel_layer

from morfix_django_restapi.settings import redis_client

channel_layer = get_channel_layer()  # Получаем channel_layer один раз на уровне модуля

# Настройка клиента Redis

def user_in_chat(user_id, chat_id):
    # Проверяем наличие пользователя в Redis
    return redis_client.sismember(f"chat_{chat_id}_active_users", str(user_id))


@receiver(post_save, sender=Message)
def on_message_created(sender, instance, created, **kwargs):
    if created:
        chat = instance.chat

        message_sender_profile = instance.sender.profiles.first()


        if message_sender_profile:
            last_message_first_name = message_sender_profile.first_name
        else:
            last_message_first_name = None

        # Обработка непрочитанных сообщений, если пользователь не в чате
        for user in chat.users.all():
            # Создание события только для пользователей, не находящихся в чате
            if not user_in_chat(chat_id=chat.id, user_id=user.id):  # Проверяем статус через флаг или иной механизм
                ChatEvent.objects.create(chat=chat, message=instance, user=user, is_read=False)
                # Получения списка непрочитанных чатов
                unseen_chats_count = count_unseen_chats(user=user)
                # Отправка количество непрочитанных чатов пользователя
                async_to_sync(channel_layer.group_send)(
                    f"user_{user.id}",
                    {
                        "type": "send.unseen.chats",
                        # Количество нерпочитанных чатов пользователя
                        "unseen_chats": int(unseen_chats_count),
                    }
                )


            # Отправка обновления списка чатов
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    "type": "send.event.update",
                    "chat_id": chat.id,
                    'last_message_first_name': last_message_first_name if user.id != instance.sender.id else "Вы",  # Имя профиля последнего сообщения в чате
                    'last_message_text': instance.text,# Текст последнего сообщения
                    'last_message_datetime': instance.datetime.isoformat(), # Дата и время последнего сообщений
                    'unseen_messages_length': ChatEvent.objects.filter(chat=chat, user=user, is_read=False).count(), # Количество непрочитанных сообщений в чате
                }
            )

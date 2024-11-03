# chat/consumers.py
from django.utils import timezone

from channels.db import database_sync_to_async

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import Chat, Message, ChatUser

from .serializers import MessageSerializer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        # Присоединение к комнате группы
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Получение пользователя
        user = self.scope["user"]

        # Получение чата по id
        chat = await database_sync_to_async(Chat.objects.get)(pk=self.chat_id)

        # Обновление поля "last_seen" экземпляра чата данного пользователя
        await self.update_chat_user(user=user, chat=chat)

        await self.accept()


    async def disconnect(self, close_code):
        # Получение пользователя
        user = self.scope["user"]

        # Получение чата по id
        chat = await database_sync_to_async(Chat.objects.get)(pk=self.chat_id)

        # Обновление поля "last_seen" перед выходом
        await self.update_chat_user(user=user, chat=chat)
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    # Получение json от вебсокета клиента
    async def receive_json(self, content):
        # получить отправителя
        user = self.scope["user"]

        # Получение чата по id
        chat = await database_sync_to_async(Chat.objects.get)(pk=self.chat_id)

        # Получаем действие
        action = content.get("action", None)
        # Получаем данные
        data = content.get("data", None)
        # Если действие равно "отправить"
        if action == "send":
            # Получаем текст по ключу "text"
            text = data.get("text", None)
            # Получаем медиа по ключу "media"
            media = data.get("media", None)

            # создание экземпляра сообщения
            message = await database_sync_to_async(Message.objects.create)(
                chat=chat,
                sender=user,
                text=text,
                media=media, # Привязываем медиафайл, если он есть
            )

            # Обновление поля "last_seen" экземпляра чата данного пользователя
            await self.update_chat_user(user=user, chat=chat)

            # Отправить сообщение в группу комнаты
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    # По ключу type прописываем в значение название метода данного потребителя (consumer),
                    # это вызовет данный метод, но если метод называется chat_message_send,
                    # в значение нужно написать: chat.message.send,
                    # т. е. вместо "_" используем "."
                    "type": "chat.message.send",
                    # Отправляем экземпляр текущего сообщения
                    "message": message,
                },
            )
            if action == "edit":
                # ID сообщения
                message_id = data.get("message_id", None)
                # Получаем текст по ключу "text"
                text = data.get("text", None)
                # Получаем медиа по ключу "media"
                media = data.get("media", None)

                # Редактирование экземпляра сообщения
                message = await self.edit_message(user=user, message_id=message_id, text=text, media=media)

                # Обновление поля "last_seen" экземпляра чата данного пользователя
                await self.update_chat_user(user=user, chat=chat)

                # Отправить сообщение в группу комнаты
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        # По ключу type прописываем в значение название метода данного потребителя (consumer),
                        # это вызовет данный метод, но если метод называется chat_message_send,
                        # в значение нужно написать: chat.message.send,
                        # т. е. вместо "_" используем "."
                        "type": "chat.message.edit",
                        # Отправляем экземпляр текущего сообщения
                        "message": message,
                    },
                )
            if action == "delete":
                # ID сообщения
                message_id = data.get("message_id", None)

                # Удаление экземпляра сообщения
                await self.delete_message(message_id=message_id)

                # Обновление поля "last_seen" экземпляра чата данного пользователя
                await self.update_chat_user(user=user, chat=chat)

                # Отправить сообщение в группу комнаты
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        # По ключу type прописываем в значение название метода данного потребителя (consumer),
                        # это вызовет данный метод, но если метод называется chat_message_send,
                        # в значение нужно написать: chat.message.send,
                        # т. е. вместо "_" используем "."
                        "type": "chat.message.delete",
                        # ID сообщения, которое было удалено
                        "message_id": message_id,
                    },
                )



    #Декоратор для базы данных из синхронности в асинхронность
    @database_sync_to_async
    # Обновление chat_user
    def update_chat_user(self, chat, user):
        # Находим запись для chat и user
        chat_user = ChatUser.objects.get(chat=chat, user=user)
        # Обновляем поле date_joined
        chat_user.last_seen = timezone.now()
        # Сохраняем изменение только поля last_seen у модели chat_user
        chat_user.save(update_fields=["last_seen"])


    @database_sync_to_async
    # Редактирование сообщения
    def edit_message(self, user, message_id, text, media):
        message = Message.objects.filter(id=message_id, sender=user).first()
        if message:
            message.text = text
            message.media = media
            message.datetime = timezone.now()
            message.save(update_fields=["text", "media", "datetime"])

        return message


    @database_sync_to_async
    # Удаление сообщения
    def delete_message(self, message_id):
        message = Message.objects.filter(id=message_id).first()
        if message:
            message.delete()



    # Получение сообщения от группы комнаты для его отправки
    async def chat_message_send(self, event):
        # Получение объекта message
        message = event.get("message", None)

        # Отправка json с только что созданным сообщением обратно в Websockets
        await self.send_json(
            {
                "action": "send",
                "message": MessageSerializer(message).data,
            }
        )


    # Получение сообщения от группы комнаты для его редактирования
    async def chat_message_edit(self, event):
        # Получение объекта message
        message = event.get("message", None)

        # Отправка json с только что измененным сообщением обратно в Websockets
        await self.send_json(
            {
                "action": "edit",
                "message": MessageSerializer(message).data,
            }
        )


    # Получение сообщения от группы комнаты для его удаления
    async def chat_message_delete(self, event):
        # Получение объекта message
        message_id = event.get("message_id", None)

        # Отправка json с только что удаленным сообщением обратно в Websockets
        await self.send_json(
            {
                "action": "delete",
                "message_id": message_id,
            }
        )
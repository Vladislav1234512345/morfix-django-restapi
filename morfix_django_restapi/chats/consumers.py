# chat/consumers.py
from django.utils import timezone

from channels.db import database_sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Chat, Message, ChatEvent

from .serializers import MessageSerializer

from morfix_django_restapi.settings import redis_client

import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        if 'error' in self.scope:
            # Вызываем функцию, которая отправит сообщение об ошибке и закроет соединение
            await self.send_error_and_close_connection(error=self.scope['error'])
        else:
            # Получение пользователя
            self.user = self.scope["user"]

            self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]

            try:
                self.chat = await database_sync_to_async(Chat.objects.get)(id=self.chat_id)
            except Chat.DoesNotExist:
                self.chat = None

            if self.chat:
                    if  await self.is_user_in_chat_users():

                        self.room_group_name = f"chat_{self.chat_id}"

                        # Присоединение к комнате группы
                        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

                        # Помечаем пользователя как активного в этом чате
                        redis_client.sadd(f"chat_{self.chat_id}_active_users", str(self.user.id))

                        await self.accept()

                    else:
                        await self.send_error_and_close_connection(error="Данный пользователь не имеет доступа к этому чату.")
            else:
                await self.send_error_and_close_connection(error="Данного чата не существует")


    async def disconnect(self, close_code):

        if not 'error' in self.scope:

            if self.chat and await self.is_user_in_chat_users():

                # Покинуть комнату группы
                await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

                # Убираем пользователя из списка активных
                redis_client.srem(f"chat_{self.chat_id}_active_users", str(self.user.id))


    # Получение json от вебсокета клиента
    async def receive(self, text_data):


        if self.chat and await self.is_user_in_chat_users():
            content = json.loads(text_data)

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
                    chat=self.chat,
                    sender=self.user,
                    text=text,
                    media=media, # Привязываем медиафайл, если он есть
                )


                message_data = MessageSerializer(message).data

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
                        "message": message_data,
                    },
                )
            elif action == "edit":
                # ID сообщения
                message_id = data.get("message_id", None)

                # Получаем текст по ключу "text"
                text = data.get("text", None)

                # Получаем медиа по ключу "media"
                media = data.get("media", None)


                # Редактирование экземпляра сообщения
                message = await self.edit_message(message_id=message_id, text=text, media=media)


                message_data = MessageSerializer(message).data

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
                        "message": message_data,
                    },
                )
            elif action == "delete":
                # ID сообщения
                message_id = data.get("message_id", None)


                # Удаление экземпляра сообщения
                await self.delete_message(message_id=message_id)


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


    @database_sync_to_async
    def is_user_in_chat_users(self):
        return self.chat.users.filter(id=self.user.id).exists()

    @database_sync_to_async
    # Редактирование сообщения
    def edit_message(self, message_id, text, media):
        message = Message.objects.filter(id=message_id, sender=self.user).first()
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
        await self.send(text_data=json.dumps({
                "action": "send",
                "message": message,
            }, ensure_ascii=False)
        )


    # Получение сообщения от группы комнаты для его редактирования
    async def chat_message_edit(self, event):
        # Получение объекта message
        message = event.get("message", None)

        # Отправка json с только что измененным сообщением обратно в Websockets
        await self.send(text_data=json.dumps({
                "action": "edit",
                "message": message,
            }, ensure_ascii=False)
        )


    # Получение сообщения от группы комнаты для его удаления
    async def chat_message_delete(self, event):
        # Получение объекта message
        message_id = event.get("message_id", None)

        # Отправка json с только что удаленным сообщением обратно в Websockets
        await self.send(text_data=json.dumps({
                "action": "delete",
                "message_id": message_id,
            }, ensure_ascii=False)
        )


    async def send_error_and_close_connection(self, error: str):

        await self.accept()

        await self.send(text_data=json.dumps({"error": error}, ensure_ascii=False))

        await self.close()





class ChatListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if 'error' in self.scope:
            # Вызываем функцию, которая отправит сообщение об ошибке и закроет соединение
            await self.send_error_and_close_connection(error=self.scope['error'])
        else:
            self.user = self.scope['user']

            if self.user.is_authenticated:
                # Обновление активности пользователя при подключении
                await self.update_user(is_online=True)

                self.group_name = f"user_{self.user.id}"

                await self.channel_layer.group_add(self.group_name, self.channel_name)

                redis_client.sadd('active_users', str(self.user.id))

                await self.accept()

                unseen_chats_count = await self.count_unseen_chats()

                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        # По ключу type прописываем в значение название метода данного потребителя (consumer),
                        # это вызовет данный метод, но если метод называется chat_message_send,
                        # в значение нужно написать: chat.message.send,
                        # т. е. вместо "_" используем "."
                        "type": "send.unseen.chats",
                        # Количество нерпочитанных чатов пользователя
                        "unseen_chats_count": int(unseen_chats_count),
                    },
                )
            else:
                await self.send_error_and_close_connection(error="Пользователь не может посмотреть чаты, пока не авторизуется.")


    async def disconnect(self, close_code):
        if not 'error' in self.scope:
            if self.user.is_authenticated:
                # Обновление активности пользователя при отключении
                await self.update_user(is_online=False)

                await self.channel_layer.group_discard(self.group_name, self.channel_name)

                redis_client.srem('active_users', str(self.user.id))

    # Асинхронная функция для отправки обновления о непрочитанных сообщениях для каждого чата
    async def send_event_update(self, event):
        # Отправляем обновление о непрочитанных сообщениях для каждого чата
        await self.send(text_data=json.dumps(event, ensure_ascii=False))

    # Асинхронная функция для отправки обновления активности каждого пользователя собеседника
    async def send_active_users(self, event):
        event["chats_users_activity"] = await self.get_chats_users_activity()

        # Отправляем обновление активности каждого пользователя собеседника
        await self.send(text_data=json.dumps(event, ensure_ascii=False))

    # Асинхронная функция для отправки количества непрочитанных чатов пользователем
    async def send_unseen_chats(self, event):
        # Отправляем количество непрочитанных чатов пользователем
        await self.send(text_data=json.dumps(event, ensure_ascii=False))


    async def send_error_and_close_connection(self, error: str):

        await self.accept()

        await self.send(text_data=json.dumps({"error": error}, ensure_ascii=False))

        await self.close()


    @database_sync_to_async
    # Получение активности пользователей чатов
    def get_chats_users_activity(self):
        chats = self.user.chats.all()
        # Данные активности пользователей чатов
        chats_users_activity_data = []
        # Цикл чатов
        for chat in chats:
            try:
                # Пользователь-собеседник чата
                other_user = chat.users.exclude(id=self.user.id).first()
            except:
                other_user = None
            # Добавление словаря в список с данными активности пользователей чатов
            chats_users_activity_data.append({
                "chat_id": chat.id,
                "other_user_is_online": other_user.is_online if other_user is not None else None,
                "other_user_last_activity": other_user.last_activity.isoformat() if other_user is not None else None,
            })

        return chats_users_activity_data


    @database_sync_to_async
    # Редактирование активности пользователя
    def update_user(self, is_online: bool):
        # Последняя актинвость = сейчас()
        self.user.last_activity = timezone.now()
        # Активность пользователя = Верно
        self.user.is_online = is_online
        # Сохраняем изменение только нескольких полей
        self.user.save(update_fields=['last_activity', 'is_online'])


    @database_sync_to_async
    # Функция подсчёта непрочитанных чатов
    def count_unseen_chats(self):
        # Получаем все непрочитанные сообщения всех чатов по user, а также чтобы они были непрочитаны
        chat_events = ChatEvent.objects.filter(user=self.user, is_read=False)
        # Создаем список из всех id чатов каждого chat_event, а затем при помощи set оставляем только уникальные
        # Возвращаем количество уникальных id чатов, что и будет равно количеству непрочитанных чатов пользователем
        return len(set([chat_event.chat.id for chat_event in chat_events]))

# from django.db import models
from django.contrib.gis.db import models

from users.models import User

# Create your models here.

class ChatUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    invite_reason = models.CharField(max_length=255)

    class Meta:
        db_table = 'chat_users'
        verbose_name = 'Пользователь чата'
        verbose_name_plural = 'Пользователи чата'
        unique_together = ('user', 'chat')

    def __str__(self):
        return f"{self.user.username} - {self.chat.id}"


class Chat(models.Model):
    name = models.CharField(verbose_name='Имя чата', max_length=50, null=True, blank=True)
    image = models.ImageField(verbose_name="Изображение чата", upload_to='images/', null=True, blank=True)
    is_group = models.BooleanField(verbose_name="Чат является группой", default=False)
    users = models.ManyToManyField(User, related_name='chats', through='ChatUser')

    def __str__(self):
        return f"{self.id}"

    class Meta:
        db_table = 'chats'
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=5000)
    media = models.FileField(upload_to='chat_media/', blank=True, null=True)  # Поле для медиафайлов

    class Meta:
        db_table = 'messages'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'



    def __str__(self):
        return (f"отправитель: {self.sender.username}\n"
                f"chat_id: {self.chat.id}\n"
                f"message_id: {self.id}"
                )



class ChatEvent(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_events")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="message_events")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_events")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'chat_events'
        verbose_name = 'Событие чата'
        verbose_name_plural = 'События чата'
        unique_together = ('chat', 'message', 'user')
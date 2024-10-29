from django.core.cache.backends.base import get_key_func
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message, ChatUser
from .serializers import ChatSerializer, MessageSerializer

from profiles.models import Profile

# Представление списка чатов
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chats_list(request):
    # Получения списка экзмепляров чатов текущего пользователя
    chats_user = ChatUser.objects.filter(user=request.user)
    # Список данных чатов пользователя
    chats_user_data = []

    # Цикл чатов пользователя
    for chat_user in chats_user:
        # Список всех сообщений пользователя
        messages = Message.objects.filter(chat=chat_user.chat)
        # Получение экземпляра последнего сообщения пользователя
        last_message = messages.order_by('datetime').last()
        # Список непрочитанных сообщений пользователя
        unseen_messages = messages.filter(datetime__gt=chat_user.last_seen)

        try:
            # Получение профиля отправителя последнего сообщения
            profile = Profile.objects.get(user=last_message.sender)
            # Если отправитель последнего сообщения равен текущему пользователю
            if last_message.sender == request.user:
                # Объявление и присвоение значения переменной profile_first_name
                profile_first_name = "Вы"
            else:
                profile_first_name = profile.first_name
        except Profile.DoesNotExist:
            profile_first_name = None

        # Словарь с данными чата
        chat_data = {
            'chat_id': chat_user.chat.id, # ID чата
            'last_message_text': last_message.text if last_message else None,# Текст последнего сообщения
            'last_message_datetime': last_message.datetime.strftime('%H:%M') if last_message else None, # Дата и время последнего сообщений
            'unseen_messages_length': unseen_messages.count(), # Количество непрочитанных сообщений в масле
            'profile_first_name': profile_first_name, # Имя профиля последнего сообщения в чате
        }
        # Добавление словаря в список
        chats_user_data.append(chat_data)
    # Возвращение ответа с данными чатов пользователя и статусом кода 200
    return Response(chats_user_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_room(request, chat_id):

    chat = Chat.objects.get(id=chat_id)

    if request.user not in chat.users.all():
        return Response({"detail": "Пользователь не является членом данного чата."}, status=status.HTTP_403_FORBIDDEN)

    messages = chat.messages.all()
    messages_data = MessageSerializer(messages, many=True).data

    return Response(
        messages_data,
        status=status.HTTP_200_OK
    )


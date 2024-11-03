from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message, ChatUser
from .serializers import MessageSerializer

from profiles.models import Profile, ProfileImage

from profiles.serializers import ProfileImageSerializer

# Представление списка чатов
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chats_list(request):
    current_user = request.user
    # Получения списка экзмепляров чатов текущего пользователя
    chats = current_user.chats.all()
    # Список данных чатов пользователя
    chats_data = []

    # Цикл чатов пользователя
    for chat in chats:
        # Список всех сообщений пользователя
        messages = Message.objects.filter(chat=chat)
        # Получение экземпляра последнего сообщения пользователя
        last_message = messages.order_by('datetime').last()
        try:
            current_chat_user = ChatUser.objects.get(chat=chat, user=current_user)
            # Список непрочитанных сообщений пользователя
            unseen_messages = messages.filter(datetime__gt=current_chat_user.last_seen)
        except:
            unseen_messages = None

        try:
            # Если отправитель последнего сообщения равен текущему пользователю
            if last_message.sender == request.user:
                # Объявление и присвоение значения переменной last_message_first_name
                last_message_first_name = "Вы"
            else:
                # Получение профиля отправителя последнего сообщения
                profile = Profile.objects.get(user=last_message.sender)
                last_message_first_name = profile.first_name
        except:
            last_message_first_name = None

        try:
            other_user = chat.users.all().exclude(id=current_user.id).first()
            other_profile = Profile.objects.get(user=other_user)
            # Получение имени собеседника чата
            other_profile_first_name = other_profile.first_name
        except:
            other_profile = None
            other_profile_first_name = None

        try:
            # Экзмемпляр фото прфоиля собеседника
            other_profile_image = ProfileImage.objects.get(profile=other_profile, is_main_image=True).image
        except:
            other_profile_image = None

        # Словарь с данными чата
        chat_data = {
            'chat_id': chat.id, # ID чата
            'other_profile_image': other_profile_image,  # Изображение профиля собеседника чата
            'other_profile_first_name': other_profile_first_name,  # Имя профиля собеседника чата
            'last_message_first_name': last_message_first_name,  # Имя профиля последнего сообщения в чате
            'last_message_text': last_message.text if last_message else None,# Текст последнего сообщения
            'last_message_datetime': last_message.datetime.strftime('%H:%M') if last_message else None, # Дата и время последнего сообщений
            'unseen_messages_length': unseen_messages.count(), # Количество непрочитанных сообщений в чате
        }
        # Добавление словаря в список
        chats_data.append(chat_data)
    # Возвращение ответа с данными чатов пользователя и статусом кода 200
    return Response(chats_data, status=status.HTTP_200_OK)



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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# Контроллер активности пользователей чата
def chats_users_activity(request):
    # Текущий пользователь
    current_user = request.user
    # Чаты текущего пользователя
    chats = current_user.chats.all()
    # Данные активности пользователей чатов
    chats_users_activity_data = []
    # Цикл чатов
    for chat in chats:
        try:
            # Последняя активность другого пользователя чата
            other_user_is_online = chat.users.exclude(id=current_user.id).first().is_online
        except:
            other_user_is_online = None
        # Добавление словаря в список с данными активности пользователей чатов
        chats_users_activity_data.append({
            "chat_id": chat.id,
            "other_user_is_online": other_user_is_online
        })
    # Возвращение ответа с данными активности пользователей чатов и статусом кода 200
    return Response(chats_users_activity_data, status=status.HTTP_200_OK)



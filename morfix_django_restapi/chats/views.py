from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message, ChatEvent
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
            unseen_messages = ChatEvent.objects.filter(user=current_user, chat=chat, is_read=False)
            # количество непрочитанных сообщений
            unseen_messages_count = len(unseen_messages)
        except:
            unseen_messages_count = None

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
            other_profile_image = ProfileImageSerializer(
                ProfileImage.objects.get(
                    profile=other_profile,
                    is_main_image=True
                )
            ).data.get("image")
        except:
            other_profile_image = None

        # Словарь с данными чата
        chat_data = {
            'chat_id': chat.id, # ID чата
            'other_profile_id': other_profile.id if other_profile is not None else None, # ID профиля собеседника
            'other_profile_image': other_profile_image,  # Изображение профиля собеседника чата
            'other_profile_first_name': other_profile_first_name,  # Имя профиля собеседника чата
            'last_message_first_name': last_message_first_name,  # Имя профиля последнего сообщения в чате
            'last_message_text': last_message.text if last_message else None,# Текст последнего сообщения
            'last_message_datetime': last_message.datetime if last_message else None, # Дата и время последнего сообщений
            'unseen_messages_length': unseen_messages_count, # Количество непрочитанных сообщений в чате
        }
        # Добавление словаря в список
        chats_data.append(chat_data)
    # Возвращение ответа с данными чатов пользователя и статусом кода 200
    return Response(chats_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_room(request, chat_id):

    chat = Chat.objects.get(id=chat_id)

    unseen_messages = ChatEvent.objects.filter(user=request.user, chat=chat, is_read=False).order_by('-id')

    if unseen_messages:
        # Удаляем экземпляра событий чата данного пользователя данного чата
        unseen_messages.delete()

    if request.user not in chat.users.all():
        return Response({"detail": "Пользователь не является членом данного чата."}, status=status.HTTP_403_FORBIDDEN)

    messages = chat.messages.all()
    messages_data = MessageSerializer(messages, many=True).data

    return Response(
        messages_data,
        status=status.HTTP_200_OK
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_chat(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        raise Http404({"detail": "Данного чата не существует."})

    if request.user not in chat.users.all():
        return Response({"detail": "У вас нет прав удалить данный чат."}, status=status.HTTP_403_FORBIDDEN)

    chat.delete()

    return Response({"detail": "Чат успешно удален."}, status=status.HTTP_200_OK)



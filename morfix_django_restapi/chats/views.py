from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message, ChatUser
from .serializers import ChatSerializer, MessageSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chats_list(request):
    user = request.user
    chats_user = ChatUser.objects.filter(user=user)
    chats_user_data = []

    for chat_user in chats_user:
        unseen_messages = Message.objects.filter(chat=chat_user.chat, datetime__gt=chat_user.last_seen)
        last_message = unseen_messages.order_by('datetime').last()

        chat_data = {
            'chat_id': chat_user.chat.id,
            'last_message_text': last_message.text if last_message else None,
            'messages_length': unseen_messages.count(),
            'last_seen': chat_user.last_seen,
        }

        chats_user_data.append(chat_data)

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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Chat, Message, ChatUsers
from .serializers import ChatSerializer, MessageSerializer


class ChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Возвращает список чатов для текущего пользователя.
        """
        user = request.user
        chats = ChatUsers.objects.filter(user=user)
        chats_list = []

        for chat_user in chats:
            messages = Message.objects.filter(chat=chat_user.chat, datetime__gt=chat_user.last_seen)
            last_message = messages.order_by('datetime').last()

            chat_data = {
                'chat_id': chat_user.chat.id,
                'last_message_text': last_message.text if last_message else None,
                'messages_length': messages.count(),
                'last_seen': chat_user.last_seen,
            }
            chats_list.append(chat_data)

        return Response({"chats": chats_list})


class ChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        """
        Возвращает детали чата и сообщения.
        """
        chat = Chat.objects.get(id=chat_id)
        if request.user not in chat.users.all():
            return Response({"detail": "Unauthorized"}, status=403)

        messages = chat.messages.all()
        serialized_messages = MessageSerializer(messages, many=True)

        return Response({
            "chat_id": chat_id,
            "messages": serialized_messages.data,
        })

    def post(self, request, chat_id):
        """
        Отправка сообщения в чат.
        """
        chat = Chat.objects.get(id=chat_id)
        if request.user not in chat.users.all():
            return Response({"detail": "Unauthorized"}, status=403)

        text = request.data.get('message')
        if text:
            message = Message.objects.create(chat=chat, sender=request.user, text=text)
            return Response({"message": "Message sent", "message_id": message.id})
        return Response({"error": "No message content"}, status=400)


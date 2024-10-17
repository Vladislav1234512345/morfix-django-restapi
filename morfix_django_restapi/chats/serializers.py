from rest_framework import serializers

from .models import Chat, ChatUser, Message


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name', 'image', 'is_group']


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ['id', 'chat', 'user', 'date_joined', 'invite_reason', 'last_seen']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'datetime', 'text', 'media']
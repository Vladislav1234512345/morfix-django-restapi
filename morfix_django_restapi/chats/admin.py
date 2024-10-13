from django.contrib import admin

from .models import Chat, ChatUsers, Message

# Register your models here.

admin.site.register(Chat)
admin.site.register(ChatUsers)
admin.site.register(Message)

from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.chats_list, name='chats-list'),
    path('users-activity/', views.chats_users_activity, name='users-activity'),
    path('<int:chat_id>/', views.chat_room, name='chat-room'),
]
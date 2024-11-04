from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.chats_list, name='chats-list'), # Список чатов текущего профиля
    path('users-activity/', views.chats_users_activity, name='users-activity'), # Список активности профилей собеседников
    path('<int:chat_id>/', views.chat_room, name='chat'), # Данные определенного чата
    path('<int:chat_id>/delete/', views.delete_chat, name='chat'), # Удаление чата
]
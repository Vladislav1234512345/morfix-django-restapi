from chats.models import ChatEvent


def count_unseen_chats(user):
    # Получаем все непрочитанные сообщения всех чатов по user, а также чтобы они были непрочитаны
    chat_events = ChatEvent.objects.filter(user=user, is_read=False)
    # Создаем список из всех id чатов каждого chat_event, а затем при помощи set оставляем только уникальные
    # Возвращаем количество уникальных id чатов, что и будет равно количеству непрочитанных чатов пользователем
    return len(set([chat_event.chat.id for chat_event in chat_events]))

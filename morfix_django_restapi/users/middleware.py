from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


# Middleware класс для отслеживания активности пользователя
class ActiveUserMiddleware(MiddlewareMixin):
    # Функция которая запрашивает данные
    def process_request(self, request):
        # Условие, если пользователь авторизован
        if request.user.is_authenticated:
            # Дата и время сейчас
            now = timezone.now()
            # Текущий пользователь из запроса
            user = request.user
            # Последняя активность пользователя = сейчас
            user.last_activity = now
            # Активность пользователя = да
            user.is_active = True
            # Сохраняем изменение только нескольких полей
            user.save(update_fields=['last_activity', 'is_active'])

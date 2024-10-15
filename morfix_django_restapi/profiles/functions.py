from django.http import Http404

from .models import Profile


def get_profile(request):
    # Получение экземпляра профиля по пользователю, который отправил запрос
    try:
        return Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        raise Http404("Профиль не был создан.")

from django.http import Http404
from rest_framework.generics import get_object_or_404


from .models import Profile, ProfileImage, ProfileHobby
from .serializers import ProfileSerializer, ProfileImageSerializer


def get_profile(request):
    # Получение экземпляра профиля по пользователю, который отправил запрос
    try:
        return Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        raise Http404("Профиль не был создан.")


def get_profile_full_info_data(profile):
    # Получение данных профиля
    profile_data = ProfileSerializer(profile).data
    # Добавление ключ username и его значение
    profile_data["username"] = profile.user.username

    profile_hobbies = ProfileHobby.objects.filter(profile=profile).all()

    profile_hobbies_data = []

    for profile_hobby in profile_hobbies:
        profile_hobby_dict = {
            "id": profile_hobby.id,
            "name": profile_hobby.hobby.name,
        }

        profile_hobbies_data.append(profile_hobby_dict)

    profile_data["hobbies"] = profile_hobbies_data

    profile_images = ProfileImage.objects.filter(profile=profile).all()

    profile_images_data = ProfileImageSerializer(profile_images, many=True).data

    profile_data["images"] = profile_images_data

    return profile_data

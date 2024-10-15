import json
import random

from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .functions import get_profile
from .serializers import ProfileSerializer, ProfileImageSerializer, ProfileHobbySerializer, HobbySerializer

from .models import Profile, ProfileImage, Hobby, ProfileHobby

# Класс создания профиля
class ProfileCreateView(generics.CreateAPIView):
    # Класс сериализатора
    serializer_class = ProfileSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]


    # Создание объекта сериализатора
    def create(self, request, *args, **kwargs):

        # Проверка существует ли профиль на данный момент
        if Profile.objects.filter(user=request.user).first():
            # Отправка ошибки 400 при уже существующем профиле
            return Response({"detail": "Профиль уже существует."}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем сериализатор
        serializer = self.get_serializer(data=request.data)
        # Проверяем данные сериализатора
        serializer.is_valid(raise_exception=True)

        # Получаем день рождения из сериализатора
        birthday = serializer.validated_data.get('birthday')

        # Получаем сегодняшний день
        today = date.today()

        # Получаем возраст
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

        # Проверяем возраст
        if int(age) < 18:
            return Response({'detail': 'Возраст должен быть 18 лет или старше.'}, status=status.HTTP_403_FORBIDDEN)

        # Создаем объект, в данном случае объект профиля
        self.perform_create(serializer)

        # Получаем заголовки при успешном выполнении
        headers = self.get_success_headers(serializer.data)

        # Возвращаем ответ с данными, заголовками и статусом кода
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# Класс обновления профиля
class ProfileUpdateView(generics.UpdateAPIView):
    # Класс сериализатора
    serializer_class = ProfileSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    # Метод получения объекта
    def get_object(self):
        return get_profile(self.request)

    # Обновление объекта сериализатора
    def update(self, request, *args, **kwargs):

        # Получение объекта профиля
        instance = self.get_object()

        # Получение сериализатора
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        # Проверка сериализатора
        serializer.is_valid(raise_exception=True)

        # Обновляем объект, в данном случае профиль
        self.perform_update(serializer)

        # Возвращаем ответ с данными, заголовками и статусом кода
        return Response(serializer.data, status=status.HTTP_200_OK)


# Класс получения данных пользователя
class ProfileRetrieveView(generics.RetrieveAPIView):
    # Класс сериализатора
    serializer_class = ProfileSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    # Метод получения объекта
    def get_object(self):
        return get_profile(self.request)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profiles(request):
    # Объект профиля
    profile = get_profile(request)

    # Количество профилей для поиска
    profiles_count = int(request.GET.get("profiles_count", 20))

    # Разрешенный размах в возрасте
    allowed_age_difference = int(request.GET.get("allowed_age_difference", 5))

    # Минимальный возраст профиля для поиска
    min_age = profile.age - allowed_age_difference

    # Максимальный возраст профиля для поиска
    max_age = profile.age + allowed_age_difference

    # Список объектов профилей для мэтча
    searching_profiles = Profile.objects.filter(
        gender=profile.searching_gender,
        searching_gender=profile.gender,
        age__range=(min_age, max_age)
    ).exclude(user=request.user).prefetch_related('images')

    # Явно указываем тип list для searching_profiles
    searching_profiles = list(searching_profiles)

    # Перемешиваем профили
    random.shuffle(searching_profiles)

    # Ограничиваем количество найденных профилей
    searching_profiles = searching_profiles[:profiles_count]

    # Список данных подходящих профилей
    searching_profiles_data = []

    # Цикл из подходящих профилей
    for searching_profile in searching_profiles:
        # Данные подходящего профиля из сериализатора
        searching_profile_data = ProfileSerializer(searching_profile).data


        #  Получаем все хобби профиля
        searching_profile_hobbies = ProfileHobby.objects.filter(profile=searching_profile)

        # Данные хобби профиля
        searching_profile_hobbies_data = []

        for searching_profile_hobby in searching_profile_hobbies:
            searching_profile_hobby_dict = {
                "id": searching_profile_hobby.id,
                "name": searching_profile_hobby.hobby.name,
            }

            searching_profile_hobbies_data.append(searching_profile_hobby_dict)

        # Добавление хобби данному профилю в сериализатор
        searching_profile_data["hobbies"] = searching_profile_hobbies_data


        # Изображение подходящих профилей
        searching_profile_images = ProfileImage.objects.filter(profile=searching_profile)
        # Данные изображений подходящих профилей из сериализатора
        searching_profile_images_data = ProfileImageSerializer(searching_profile_images, many=True).data
        # Добавление в данные подходящего профиля из сериализатора поля images,
        # который является данными изображений подходящего профиля
        searching_profile_data["images"] = searching_profile_images_data


        # Добавление данных подходящего профиля в список подходящих профилей
        searching_profiles_data.append(searching_profile_data)

    # Ответ с данными и статусом кода 200
    return Response(searching_profiles_data, status=status.HTTP_200_OK)


# Класс создания изображения профиля
class ProfileImageCreateView(generics.CreateAPIView):
    # Класс сериализатора
    serializer_class = ProfileImageSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    # Создание объекта сериализатора
    def create(self, request, *args, **kwargs):
        # Получение профиля
        get_profile(self.request)
        # Получаем сериализатор
        serializer = self.get_serializer(data=request.data)
        # Проверяем данные сериализатора
        serializer.is_valid(raise_exception=True)

        # Создаем объект, в данном случае объект profile_image
        self.perform_create(serializer)

        # Получаем заголовки при успешном выполнении
        headers = self.get_success_headers(serializer.data)

        # Возвращаем ответ с данными, заголовками и статусом кода
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# Класс удаления изображения профиля
class ProfileImageDeleteView(generics.DestroyAPIView):
    # Класс сериализатора
    serializer_class = ProfileImageSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    # Метод получения объекта profile_image
    def get_object(self):
        # Объект профиля из запроса
        profile = get_profile(self.request)
        # Получение изображения профиля по ID и проверка, что оно принадлежит профилю
        profile_image = get_object_or_404(ProfileImage, id=self.kwargs['pk'], profile=profile)
        # Возвращаем объект иозображения пользователя
        return profile_image

    # Метод удаления объекта при помощи сериализатора
    def delete(self, request, *args, **kwargs):
        # Получения объекта profile_image
        profile_image = self.get_object()
        # Удаляем изображение профиля
        profile_image.delete()
        # Отправка ответа с данными и статусом кода
        return Response({"detail": "Изображение профиля успешно удалено."}, status=status.HTTP_200_OK)


# Класс получения изображения профиля
class ProfileImageRetrieveView(generics.RetrieveAPIView):
    # Класс сериализатора
    serializer_class = ProfileImageSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Объект профиля из запроса
        profile = get_profile(self.request)
        # Получаем объект изображения по id и проверяем, что оно связано с профилем
        profile_image = get_object_or_404(ProfileImage, id=self.kwargs['pk'], profile=profile)
        # Возвращаем объект изображения профиля
        return profile_image

# Класс получения списка изображений профиля
class ProfileImageListView(generics.ListAPIView):
    # Класс сериализатора
    serializer_class = ProfileImageSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    # Метод получения списка объектов изображений профиля
    def get_queryset(self):
        # Объект профиля из запроса
        profile = get_profile(self.request)
        # Изображения профиля по профилю
        profile_images = ProfileImage.objects.filter(profile=profile).all()
        # Возвращение изображений пользователя
        return profile_images


# Класс создания хобби профиля
class ProfileHobbyCreateView(generics.GenericAPIView):
    # Класс сериализатора
    serializer_class = ProfileHobbySerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Получение профиля
        get_profile(self.request)

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        profile_hobby = serializer.save()

        response = {
            "id": profile_hobby.id,
            "name": profile_hobby.hobby.name,
        }

        return Response(response, status=status.HTTP_201_CREATED)


class ProfileHobbyListView(generics.ListAPIView):
    serializer_class = ProfileHobbySerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем профиль текущего пользователя
        profile = get_profile(self.request)
        profile_hobbies = ProfileHobby.objects.filter(profile=profile)  # Получаем все ProfileHobby для данного пользователя

        profile_hobbies_list = []

        for profile_hobby in profile_hobbies:
            profile_hobby_dict = {
                "id": profile_hobby.id,
                "name": profile_hobby.hobby.name,
            }

            profile_hobbies_list.append(profile_hobby_dict)

        return profile_hobbies_list


class ProfileHobbyDeleteView(generics.DestroyAPIView):
    serializer_class = ProfileHobbySerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Объект профиля из запроса
        profile = get_profile(self.request)
        # Получение изображения профиля по ID и проверка, что оно принадлежит профилю
        profile_hobby = get_object_or_404(ProfileHobby, id=self.kwargs['pk'], profile=profile)
        # Возвращаем объект иозображения пользователя
        return profile_hobby

    # Метод удаления объекта при помощи сериализатора
    def delete(self, request, *args, **kwargs):
        # Получения объекта profile_hobby
        profile_hobby = self.get_object()
        # Удаляем хобби профиля
        profile_hobby.delete()
        # Отправка ответа с данными и статусом кода
        return Response({"detail": "Хобби профиля успешно удалено."}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_hobbies_list(request):

    hobbies = Hobby.objects.all()

    hobbies_list_data = []

    for hobby in hobbies:
        hobby_list_data = HobbySerializer(hobby).data
        hobbies_list_data.append(hobby_list_data)

    return Response(hobbies_list_data, status=status.HTTP_200_OK)



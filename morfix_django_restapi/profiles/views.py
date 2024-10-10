import random

from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ProfileSerializer, ProfileImageSerializer

from .models import Profile, ProfileImage

# Класс создания профиля
class ProfileCreateView(generics.CreateAPIView):
    # Класс сериализатора
    serializer_class = ProfileSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    # Создание объекта сериализатора
    def create(self, request, *args, **kwargs):
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
        # Получение экземпляра профиля по пользователю, который отправил запрос
        return Profile.objects.get(user=self.request.user)

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
        # Получение экземпляра профиля по пользователю, который отправил запрос
        return Profile.objects.get(user=self.request.user)


# Класс создания изображения профиля
class ProfileImageCreateView(generics.CreateAPIView):
    # Класс сериализатора
    serializer_class = ProfileImageSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    # Создание объекта сериализатора
    def create(self, request, *args, **kwargs):
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
        # Получение пользователя из запроса
        user = self.request.user
        # Получение изображения профиля по ID и проверка, что оно принадлежит пользователю
        profile_image = get_object_or_404(ProfileImage, id=self.kwargs['pk'], profile__user=user)
        # Возвращаем объект иозображения пользователя
        return profile_image

    # Метод удаления объекта при помощи сериализатора
    def delete(self, request, *args, **kwargs):
        # Получения объекта profile_image
        profile_image = self.get_object()
        # Удаляем изображение профиля
        profile_image.delete()
        # Отправка ответа с данными и статусом кода
        return Response({"detail": "Profile image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Класс получения изображения профиля
class ProfileImageRetrieveView(generics.RetrieveAPIView):
    # Класс сериализатора
    serializer_class = ProfileImageSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Получаем пользователя
        user = self.request.user
        # Получаем объект изображения по id и проверяем, что оно связано с профилем текущего пользователя
        profile_image = get_object_or_404(ProfileImage, id=self.kwargs['pk'], profile__user=user)
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
        # Объект пользователя из запроса
        user = self.request.user
        # Изображения пользователя по пользователю
        profile_images = ProfileImage.objects.filter(profile__user=user).all()
        # Возвращение изображений пользователя
        return profile_images


@api_view(['GET'])
def get_profiles(request):
    # Объект профиля
    profile = get_object_or_404(Profile, user=request.user)

    # Количество профилей для поиска
    PROFILES_COUNT = 5

    # Разрешенный размах в возрасте
    ALLOWED_AGE_DIFFERENCE = 5

    # Минимальный возраст профиля для поиска
    min_age = profile.age - ALLOWED_AGE_DIFFERENCE

    # Максимальный возраст профиля для поиска
    max_age = profile.age + ALLOWED_AGE_DIFFERENCE

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
    searching_profiles = searching_profiles[:PROFILES_COUNT]

    # Список данных подходящих профилей
    searching_profiles_data = []

    # Цикл из подходящих профилей
    for searching_profile in searching_profiles:
        # Данные подходящего профиля из сериализатора
        searching_profile_data = ProfileSerializer(searching_profile).data
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




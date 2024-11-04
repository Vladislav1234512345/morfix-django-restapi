import random

from datetime import date

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.utils import timezone

from .functions import get_profile, get_profile_full_info_data
from .serializers import ProfileSerializer, ProfileImageSerializer, ProfileHobbySerializer, HobbySerializer, \
    LikeSerializer

from .models import Profile, ProfileImage, Hobby, ProfileHobby, Like

from chats.models import Chat, ChatUser

from chats.serializers import ChatSerializer


class ProfileHobbyListCreateView(generics.ListCreateAPIView):
    # Класс сериализатора
    serializer_class = ProfileHobbySerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем профиль текущего пользователя
        profile = get_profile(self.request)
        profile_hobbies = ProfileHobby.objects.filter(
            profile=profile)  # Получаем все ProfileHobby для данного пользователя

        profile_hobbies_list = []

        for profile_hobby in profile_hobbies:
            profile_hobby_dict = {
                "id": profile_hobby.id,
                "name": profile_hobby.hobby.name,
            }

            profile_hobbies_list.append(profile_hobby_dict)

        return profile_hobbies_list

    def create(self, request, *args, **kwargs):
        # Проверяем, что пришел список объектов
        if not isinstance(request.data, list):
            return Response({"error": "Ожидается список хобби профиля."}, status=status.HTTP_400_BAD_REQUEST)

        if len(request.data) == 0:
            return Response({"error": "Список хобби не должен быть пустым."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем сериализатор с контекстом запроса
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        # Сохраняем данные
        self.perform_create(serializer)

        profile_hobbies_data = []

        for profile_hobby in serializer.instance:
            profile_hobbies_data.append({
                "id": profile_hobby.id,
                "name": profile_hobby.hobby.name,
            })

        return Response(profile_hobbies_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Сохраняем объекты хобби, передавая профиль
        profile = get_profile(self.request)
        serializer.save(profile=profile)

# Класс создания хобби профиля
class ProfileHobbyCreateView(generics.GenericAPIView):
    # Класс сериализатора
    serializer_class = ProfileHobbySerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Получение профиля
        get_profile(request)

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        profile_hobby = serializer.save()

        response = {
            "id": profile_hobby.id,
            "name": profile_hobby.hobby.name,
        }

        return Response(response, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_profile_hobbies(request):
#     get_profile(request)
#
#     # Проверяем, что пришел список объектов
#     if not isinstance(request.data, list):
#         return Response({"error": "Ожидается список хобби профиля."}, status=status.HTTP_400_BAD_REQUEST)
#
#     if len(request.data) == 0:
#         return Response({"error": "Список хобби не должен быть пустым."}, status=status.HTTP_400_BAD_REQUEST)
#
#     serializer = ProfileHobbySerializer(data=request.data, many=True)
#
#     serializer.is_valid(raise_exception=True)
#
#     profile_hobbies = serializer.save()
#
#     profile_hobbies_data = []
#
#     for profile_hobby in profile_hobbies:
#         profile_hobbies_data.append({
#             "id": profile_hobby.id,
#             "name": profile_hobby.hobby.name,
#         })
#
#     return Response(profile_hobbies_data, status=status.HTTP_201_CREATED)



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


# Класс создания изображения профиля
class ProfileImageCreateView(generics.CreateAPIView):
    # Класс сериализатора
    serializer_class = ProfileImageSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    # Создание объекта сериализатора
    def create(self, request, *args, **kwargs):
        # Получение профиля
        profile = get_profile(self.request)
        # Получаем сериализатор
        serializer = self.get_serializer(data=request.data)
        # Проверяем данные сериализатора
        serializer.is_valid(raise_exception=True)

        # Создаем объект, в данном случае объект profile_image
        self.perform_create(serializer)

        # Если данный экземпляр изображения профиля являеться главным,
        # тогда изменяем все другие экземпляры изображений профиля, которые были главными
        if serializer.data["is_main_image"] == True:
                profile_images = ProfileImage.objects.filter(
                    profile=profile,
                    is_main_image=True
                ).exclude(id=serializer.data["id"])
                profile_images.update(is_main_image=False)

        # Получаем заголовки при успешном выполнении
        headers = self.get_success_headers(serializer.data)

        # Возвращаем ответ с данными, заголовками и статусом кода
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# Класс обновления изображения профиля
class ProfileImageUpdateView(generics.UpdateAPIView):
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

        # Если данный экземпляр изображения профиля являеться главным,
        # тогда изменяем все другие экземпляры изображений профиля, которые были главными
        if serializer.data["is_main_image"] == True:
                profile_images = ProfileImage.objects.filter(
                    profile=instance.profile,
                    is_main_image=True
                ).exclude(id=serializer.data["id"])
                profile_images.update(is_main_image=False)

        # Возвращаем ответ с данными, заголовками и статусом кода
        return Response(serializer.data, status=status.HTTP_200_OK)


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
def profile_full_info(request, profile_id):
    try:
        # Экземпляр профиля по его id
        profile = Profile.objects.get(id=profile_id)
        if profile.user == request.user:
            return Response(
                {
                    "detail": "Для просмотра профиля текущего пользователя используйте /full-info/me/ ednpoint."
                },
                status=status.HTTP_200_OK
            )
    except:
        return Response({"detail": "Данный профиль не найден."}, status=status.HTTP_404_NOT_FOUND)

    # Получение полных данных профиля
    profile_data = get_profile_full_info_data(profile)

    return Response(profile_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile_full_info(request):
    # Получение экземпляра профиля текущего пользователя
    profile = get_profile(request)
    # Получение полных данных профиля
    profile_data = get_profile_full_info_data(profile)

    return Response(profile_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_profiles(request):
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
        is_active=True,
        dating_purpose=profile.dating_purpose,
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
        # Получение полной информации искомого профиля
        searching_profile_data = get_profile_full_info_data(searching_profile)

        # Добавление данных подходящего профиля в список подходящих профилей
        searching_profiles_data.append(searching_profile_data)

    # Ответ с данными и статусом кода 200
    return Response(searching_profiles_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def received_likes_profiles(request):
    # Получение экземпляра профиля текущего пользователя
    current_profile = get_profile(request)
    # Получение всех лайков данного профиля
    current_profile_likes = current_profile.received_likes.all()
    senders_likes_profiles_data = []
    # Цикл лайков данного профиля
    for current_profile_like in current_profile_likes:
        sender_like_profile_data = {
            # Получение данных текущего лайка профиля
            "like": LikeSerializer(current_profile_like).data,
            # Получение полных данных профиля, который отправил лайк профилю текущего пользователя
            "profile": get_profile_full_info_data(current_profile_like.sender),
        }
        # Добавление данных профиля в список всех данных профилей, которые лайкнули профиль текущего пользователя
        senders_likes_profiles_data.append(sender_like_profile_data)

    return Response(senders_likes_profiles_data, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_received_like(request, pk):
    try:
        current_like = Like.objects.get(pk=pk)
    except Like.DoesNotExist:
        raise Http404({"detail": "Данного лайка не существует."})

    if current_like.receiver.user == request.user:
        current_like.delete()

        return Response({"detail": "Лайк успешно удален."}, status=status.HTTP_200_OK)

    elif current_like.sender.user == request.user:
        return Response({"detail": "Вы не можете удалить свой лайк."}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"detail": "У вас нету права удалить чужой лайк."}, status=status.HTTP_403_FORBIDDEN)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_like(request):
    # Получение объекта профиля
    profile = get_profile(request)
    # Получение объекта пользователя из запроса
    user = request.user
    # Получение id профиля из post запроса
    profile_id = request.data.get("profile_id")

    if profile.id == profile_id:
        return Response({"detail": "Нельзя отправить лайк самому себе."}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка существует ли желанный профиль
    try:
        # Получения профиля по его id
        searching_profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        # Отправка ответа с статусом кода 404 в случае, если профиля не существует
        return Response({"detail": "Анкеты, которая понравилась, не существует."}, status=status.HTTP_404_NOT_FOUND)

    # Получение объекта желанного пользователя
    searching_user = searching_profile.user

    # Поиск чата с участием пользователя, который ищет, и пользователя, которого ищет первый
    chat = Chat.objects.filter(users=user).filter(users=searching_user).filter(is_group=False).first()

    # Условие, которое выполниться в случае существования чата
    if chat:
        # Отправка ответа с данными чата и статусом кода 200
        return Response(ChatSerializer(chat).data, status=status.HTTP_200_OK)

    # Поиск объекта лайк, отправителем которого является желанный профиль, а получателем данный профиль
    like = Like.objects.filter(receiver=profile, sender=searching_profile).first()

    # Если существует объект лайка
    if like:
        # Удаляем лайк из бд
        like.delete()
        # Создаем новый чат
        new_chat = Chat(is_group=False)
        # Сохраняем изменения
        new_chat.save()
        # Дата и время сейчас
        datetime_now = timezone.now()
        # Создаем объект пользователя чата с новым чатом и данным пользователем
        ChatUser.objects.create(user=user, chat=new_chat, date_joined=datetime_now, invite_reason='Создал чат.')
        # Создаем объект пользователя чата с новым чатом и желанным пользователем
        ChatUser.objects.create(user=searching_user, chat=new_chat, date_joined=datetime_now, invite_reason='Был приглашен в чат.')
        # Отправка ответа о том, что чат успешно создани, а также статус код 201
        return Response({"detail": "Чат успешно создан."}, status=status.HTTP_201_CREATED)

    # Получение или создание объекта лайка, у которого отправитель данный профиль, а получатель желанный профиль
    new_like, new_like_created = Like.objects.get_or_create(receiver=searching_profile, sender=profile)
    # Если лайк не был найден, его создали и выполняеться условие
    if new_like_created:
        # Сохранение изменения лайка
        new_like.save()
        # Отправка ответа о том, что лайк успешно создан, и статутс код 201
        return Response({"detail": "Лайк успешно создан."}, status=status.HTTP_201_CREATED)

    return Response({"detail": "Лайк уже был отправлен."}, status=status.HTTP_400_BAD_REQUEST)


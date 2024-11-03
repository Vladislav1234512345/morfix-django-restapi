from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView

from .serializers import UserSerializer

from .models import User

from django.conf import settings


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Валидация данных и создание пользователя
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Сохраняем объект, в данном случае объект пользователя
        user = serializer.save()

        # Генерация токенов
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Установка HttpOnly cookie для refresh токена
        response = Response({
            'access': access_token,
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)

        # Установим refresh токен в HttpOnly cookie
        cookie_max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
        response.set_cookie(
            key=settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH_NAME', 'default_cookie_name'),  # Укажите значение по умолчанию
            value=str(refresh),
            httponly=True,
            max_age=int(cookie_max_age),
            samesite='Lax',
            secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False)  # Включай secure, если используешь HTTPS
        )

        return response

class UserUpdateView(generics.UpdateAPIView):
    # Класс сериализатора
    serializer_class = UserSerializer
    # Разрешенные классы
    permission_classes = [IsAuthenticated]

    # Метод получения объекта
    def get_object(self):
        # Получение экземпляра пользователя по пользователю, который отправил запрос
        return self.request.user

    # Обновление объекта сериализатора
    def update(self, request, *args, **kwargs):
        # Получение объекта профиля
        instance = self.get_object()

        # Получение сериализатора
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        # Проверка сериализатора
        serializer.is_valid(raise_exception=True)

        # Обновляем объект, в данном случае пользователь
        self.perform_update(serializer)

        # Возвращаем ответ с данными, заголовками и статусом кода
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Извлекаем данные из запроса
        username = request.data.get('username')
        password = request.data.get('password')

        # Проверяем, есть ли такой пользователь
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'Пользователя с таким логином не существует.'}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем правильность пароля
        if not user.check_password(password):
            return Response({'detail': 'Неправильный пароль.'}, status=status.HTTP_400_BAD_REQUEST)

        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            refresh_token = response.data['refresh']

            cookie_max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
            response.set_cookie(
                key=settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH_NAME', 'default_cookie_name'),
                # Укажите значение по умолчанию
                value=refresh_token,
                httponly=True,
                max_age=int(cookie_max_age),
                samesite='Lax',
                secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False)  # Включай secure, если используешь HTTPS
            )

            del response.data['refresh']

            response.data['user'] = UserSerializer(user).data

        return response


class UserDeleteView(generics.DestroyAPIView):
    # Для удаления пользователя необходимо, чтобы он был аутентифицирован
    permission_classes = [IsAuthenticated]

    # Получаем текущего пользователя
    def get_object(self):
        return self.request.user

    # Переопределяем метод удаления для добавления кастомного ответа
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        self.perform_destroy(user)

        # Возвращаем успешный ответ после удаления пользователя
        return Response({"detail": "Ваш аккаунт был успешно удален."}, status=status.HTTP_200_OK)



class CustomTokenRefreshView(TokenRefreshView):

    def get(self, request, *args, **kwargs):
        # Извлечение refresh токена из куков
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH_NAME', 'refresh_token'))

        if not refresh_token:
            return Response({'detail': 'Refresh token не найден.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Передаем токен для проверки
        request.data['refresh'] = refresh_token

        # Вызываем стандартный метод TokenRefreshView (POST)
        response = super().post(request, *args, **kwargs)

        # Если запрос успешен, установим новый refresh токен в куки
        if response.status_code == status.HTTP_200_OK:
            new_refresh_token = response.data.get('refresh')

            if new_refresh_token:
                cookie_max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
                response.set_cookie(
                    key=settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH_NAME', 'refresh_token'),
                    value=new_refresh_token,
                    httponly=True,
                    max_age=int(cookie_max_age),
                    samesite='Lax',
                    secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False)
                )

                del response.data['refresh']

        return response



class UserLogoutView(APIView):
    # Для удаления refresh токена пользователя необходимо, чтобы он был аутентифицирован
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Создать объект ответа
        response = Response({"detail": "Refresh токен пользователя успешно удалён!"}, status=status.HTTP_200_OK)
        # Удалить refresh токен из cookies
        response.delete_cookie(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH_NAME', 'refresh_token'))
        # Вернуть ответ
        return response


class UserHeartBeatView(APIView):
    # Для удаления refresh токена пользователя необходимо, чтобы он был аутентифицирован
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Дата и время сейчас
        now = timezone.now()
        # Текущий пользователь из запроса
        user = request.user
        # Последняя активность пользователя = сейчас
        user.last_activity = now
        # Активность пользователя = да
        user.is_online = True
        # Сохраняем изменение только нескольких полей
        user.save(update_fields=['last_activity', 'is_online'])
        # Возвращение ответа
        return Response({"detail": "Активность текущего пользователя успешно обновлена."}, status=status.HTTP_200_OK)
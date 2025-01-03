from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserSerializer

from django.conf import settings
# Create your views here.


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

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        request.data["refresh"] = request.COOKIES.get('refresh_token')

        if not request.data.get("refresh"):
            Response({'detail': 'Refresh token не найден.'}, status=status.HTTP_401_UNAUTHORIZED)

        response = super().post(request, request.data,*args, **kwargs)

        if response.status_code == status.HTTP_200_OK:

            new_refresh_token = response.data.get("refresh")

            cookie_max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
            response.set_cookie(
                key=settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH_NAME', 'default_cookie_name'),
                # Укажите значение по умолчанию
                value=new_refresh_token,
                httponly=True,
                max_age=int(cookie_max_age),
                samesite='Lax',
                secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False)  # Включай secure, если используешь HTTPS
            )

            del response.data['refresh']

        return response

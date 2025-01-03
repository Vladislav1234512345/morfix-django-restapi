from django.urls import path
from .views import UserRegisterView, CustomTokenObtainPairView, CustomTokenRefreshView, UserUpdateView, UserDetailView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'), # Регистрация нового пользователя
    path('update/', UserUpdateView.as_view(), name='update'), # Обновление пользователя
    path('login/', CustomTokenObtainPairView.as_view(), name='login'), # Для получения access и refresh токенов при авторизации
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'), # Для обновления access токена
    path('', UserDetailView.as_view(), name='detail'), # Данные пользователя
]
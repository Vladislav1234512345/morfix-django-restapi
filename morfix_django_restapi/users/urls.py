from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserRegisterView, ProtectedView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token'), # Для получения access и refresh токенов при авторизации
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Для обновления access токена
    path('protected/', ProtectedView.as_view(), name='protected_view'), # Защищенное представление
]
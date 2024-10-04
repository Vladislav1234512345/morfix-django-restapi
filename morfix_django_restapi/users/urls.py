from django.urls import path
from .views import UserRegisterView, ProtectedView, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'), # Для получения access и refresh токенов при авторизации
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'), # Для обновления access токена
    path('protected/', ProtectedView.as_view(), name='protected_view'), # Защищенное представление
]
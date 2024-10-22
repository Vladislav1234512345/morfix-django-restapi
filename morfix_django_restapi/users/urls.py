from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'), # Регистрация нового пользователя
    path('update/', views.UserUpdateView.as_view(), name='update'), # Обновление пользователя
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'), # Для получения access и refresh токенов при авторизации
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'), # Для обновления access токена
    path('delete/', views.UserDeleteView.as_view(), name='delete'), # Удаление пользователя
    path('', views.UserDetailView.as_view(), name='info'), # Данные пользователя
]
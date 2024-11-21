"""
URL configuration for morfix_django_restapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

# Изменяем заголовки админ-панели django

# Заголовок страницы входа
admin.site.site_header = "Админ-панель DipLove"
# Заголовок страницы в браузере
admin.site.site_title = "Админ-панель DipLove"
# Заголовок на главной странице панели
admin.site.index_title = "Добро пожаловать в панель управления DipLove"

urlpatterns = [
    path('api/user/', include('users.urls')),
    path('api/profile/', include('profiles.urls')),
    path('api/chat/', include('chats.urls')),
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('admin/', permanent=True)),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


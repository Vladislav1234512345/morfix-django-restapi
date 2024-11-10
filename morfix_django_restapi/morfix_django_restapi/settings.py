"""
Django settings for morfix_django_restapi project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

from datetime import timedelta

import logging

logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_1*t3(z^!fpx9^u3w#s)um29ryz26r(cad)885)wmd71-zpt+l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Разрешенные хосты
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# ALLOWED_HOSTS = ['*']


# if os.name == 'nt':
#     # import platform
#     OSGEO4W = r"C:\OSGeo4W"
#     # if '64' in platform.architecture()[0]:
#     #     OSGEO4W += "64"
#     assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
#     os.environ['OSGEO4W_ROOT'] = OSGEO4W
#     os.environ['GDAL_DATA'] = OSGEO4W +  r"\share\gdal"
#     os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
#     GDAL_LIBRARY_PATH = OSGEO4W + r'\bin\gdal309.dll'
#     os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']
# else:  # Если это не Windows (т.е. Linux)
#     # Установите переменные окружения для GDAL и PROJ
#     os.environ['GDAL_DATA'] = '/usr/share/gdal'
#     os.environ['PROJ_LIB'] = '/usr/share/proj'
#
#     # Если у вас есть необходимость указать путь к GDAL библиотеке явно
#     GDAL_LIBRARY_PATH = '/usr/lib/libgdal.so'  # Путь может отличаться
#     os.environ['PATH'] = '/usr/bin:' + os.environ['PATH']


# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.gis', # приложение для работы с геоданными

    # Сторонние приложения
    'django_celery_beat',
    'channels',
    'corsheaders',
    'leaflet', # Для отображения объектов на карте
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # Локальные приложения
    'users',
    'profiles',
    'chats',
]

LEAFLET_CONFIG = {
    'SLD': True,  # Если вы хотите использовать стиль карты
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# # Разрешить все источники
# CORS_ALLOW_ALL_ORIGINS = True

# Разрешеннные источники
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True  # Разрешить передачу данных в куках

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]  # Разрешить все методы

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",  # Фронтенд адрес для доверенных запросов с CSRF-токеном
    "http://127.0.0.1:5173",
]

ROOT_URLCONF = 'morfix_django_restapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'morfix_django_restapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'morfix_django_restapi',
        'USER': 'postgres',
        'PASSWORD': 'root',
        # 'HOST': 'localhost',
        'HOST': 'db',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Расположение основного asgi приложения в проекте
ASGI_APPLICATION = "morfix_django_restapi.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
            # "hosts": [("localhost", 6379)],
        },
    },
}

# Модель авторизации пользователя
AUTH_USER_MODEL = 'users.User'

# Настройка аутентификации для DRF

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # Доступ по умолчанию только для авторизованных пользователей
    ),
}

# Настройка простого jwt (Javascript web token)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_COOKIE_NAME': 'access_token',  # Название cookie для токена доступа
    'AUTH_COOKIE_REFRESH_NAME': 'refresh_token',  # Название cookie для refresh токена
    'AUTH_COOKIE_SECURE': False,  # Защищенность куки
}


# Настройки для Celery
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_BEAT_SCHEDULE = {
    'mark-inactive-every-minute': {
        'task': 'users.tasks.update_inactive_users',
        'schedule': 10,  # Каждую четверь минуты
    },
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'INFO',  # Устанавливаем уровень для сообщений
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'INFO',  # Уровень логирования для всего Django
#             'propagate': True,
#         },
#
#     },
# }

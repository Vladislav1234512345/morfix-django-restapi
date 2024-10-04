Пошагавая настройка среды и проекта (Windows edition):

1. Установить виртуальную среду для проекта:
python -m venv venv

2. Активировать виртуальную среду:
venv\Scripts\activate

3. Переходим в папку django проекта:
cd morfix_django_restapi

4. При необходимости устанавливаем миграции:
python manage.py migrate

6. Создадим супер пользователя (опционально):
python manage.py createsuperuser

5. Запускаем django сервер:
python manage.py runserver





Документация API:

1. Регистрация:
url = https://127.0.0.1:8000/api/users/register/
method = POST
media type = application/json
content = {
    "username": "",
    "first_name": "",
    "last_name": "",
    "email": "",
    "password": ""
}
response = {
    "body": {
        "access": ""
        "user": {
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": ""
        }
    },
    cookies: {
            "refresh_token": ""
        }
    }
}


2. Авторизация:
url = https://127.0.0.1:8000/api/users/login/
method = POST
media type = application/json
content = {
    "username": "",
    "password": ""
}
response = {
    "body": {
        "access": ""
    },
    cookies: {
            "refresh_token": ""
        }
    }
}

3. Генерация нового refresh токена:
url = https://127.0.0.1:8000/api/users/token/refresh
method = POST
media type = application/json
content = {
}
response = {
    "body": {
        "access": ""
    },
    cookies: {
            "refresh_token": ""
        }
    }
}
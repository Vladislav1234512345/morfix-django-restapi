Пошагавая инструкция запуска проекта:
1. Запуск проект, подтянутый из GitHub (Windows edition):

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

2. Запуск docker-compose.yml файла:

   1. Скопировать с GitHub файл docker-compose.yml
   
   2. Скачать django образ данного проекта:
   docker pull vladislav1234512345/morfix-django-restapi:1.0.0
   
   3. Запустить docker-compose.yml:
   docker-compose up --build






Документация API:

1. Приложение - users:

   1. Регистрация:
   url = http://127.0.0.1:8000/api/users/register/
   method = POST
   media type = application/json
   content = {
       "username": "",
       "email": "",
       "phone": "",
       "password": ""
   }
   response = {
       "json": {
           "access": ""
           "user": {
               "id": "",
               "username": "",
               "email": "",
               "phone": ""
           }
       },
       cookies: {
               "refresh_token": ""
           }
       }
   }

   2. Авторизация:
   url = http://127.0.0.1:8000/api/users/login/
   method = POST
   media type = application/json
   content = {
       "username": "",
       "password": ""
   }
   response = {
       "json": {
           "access": "",
           "user": {
               "id": "",
               "username": "",
               "email": "",
               "phone": ""
           }
       },
       cookies: {
               "refresh_token": ""
           }
       }
   }

   3. Обновление пользователя:
   url = http://127.0.0.1:8000/api/users/update/
   method = PATCH
   media type = application/json
   content = {
       "headers": {
            "Authorization": "Bearer <jwt>"
       },
       "cookies": {
               "refresh_token": ""
           }
       },
        "body": {
            # Контент может иметь любые поля таблицы
        }
   }
   response = {
       "json": {
           "id": "",
           "username": "",
           "phone": "",
           "email": ""
       },
   }
   
   4. Данные пользователя:
   url = http://127.0.0.1:8000/api/users/
   method = GET
   media type = application/json
   content = {
       "headers": {
            "Authorization": "Bearer <jwt>"
       },
       "cookies": {
               "refresh_token": ""
           }
       },
        "body": {
        }
   }
   response = {
       "json": {
           "id": "",
           "username": "",
           "phone": "",
           "email": ""
       },
   }

   5. Генерация нового refresh токена:
   url = http://127.0.0.1:8000/api/users/token/refresh
   method = POST
   media type = application/json
   content = {
       "headers": {
            "Authorization": "Bearer <jwt>"
       },
       "cookies": {
               "refresh_token": ""
           }
       },
        "body": {
        }
   }
   response = {
       "json": {
           "access": ""
       },
       "cookies": {
               "refresh_token": ""
           }
       }
   }

2. Приложение - profiles:

    1. Создание профиля (анкеты):
    url = http://127.0.0.1:8000/api/profiles/create/
    method = POST
    media type = application/json
    content = {
       "headers": {
            "Authorization": "Bearer <jwt>"
       },
       "cookies": {
               "refresh_token": ""
           }
       },
        "body": {
           "first_name": "",
           "last_name": "",
           "gender": "",
           "birthday": "",
           "dating_purpose": "",
           "searching_gender": "",
       },
    }
    response = {
       "json": {
           "id": "",
           "first_name": "",
           "last_name": "",
           "gender": "",
           "birthday": "",
           "dating_purpose": "",
           "searching_gender": "",
           "description": "",
           "smokes_cigarettes": "",
           "drinks_alcoholics": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
       }
    } 
   2. Обновление профиля (анкеты):
   url = http://127.0.0.1:8000/api/profiles/update/
   method = PATCH
   media type = application/json
   content = {
       "headers": {
            "Authorization": "Bearer <jwt>"
       },
       "cookies": {
               "refresh_token": ""
           }
       },
        "body": {
           # Контент может иметь любые поля таблицы
       },
    }
    response = {
       "json": {
           "id": "",
           "first_name": "",
           "last_name": "",
           "gender": "",
           "birthday": "",
           "dating_purpose": "",
           "searching_gender": "",
           "description": "",
           "smokes_cigarettes": "",
           "drinks_alcoholics": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
       }
    } 
   3. Данные профиля (анкеты):
   url = http://127.0.0.1:8000/api/profiles/
   method = GET
   media type = application/json
   content = {
       "headers": {
            "Authorization": "Bearer <jwt>"
       },
       "cookies": {
               "refresh_token": ""
           }
       },
        "body": {
   
       },
    }
    response = {
       "json": {
           "id": "",
           "first_name": "",
           "last_name": "",
           "gender": "",
           "birthday": "",
           "dating_purpose": "",
           "searching_gender": "",
           "description": "",
           "smokes_cigarettes": "",
           "drinks_alcoholics": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
       }
    } 
   4. Удаление фото профиля (анкеты):
   url = http://127.0.0.1:8000/api/profiles/images/<id_фото>/delete/
   method = DELETE
   media type = application/json
   content = {
       "headers": {
            "Authorization": "Bearer <jwt>"
       },
       "cookies": {
               "refresh_token": ""
           }
       },
        "body": {
   
       },
    }
    response = {
       "json": {
           "detail": "Profile image deleted successfully."
       }
    } 
   5. Данные фото профиля (анкеты):
   url = http://127.0.0.1:8000/api/profiles/images/<id_фото>/
   method = GET
   media type = application/json
   content = {
       "headers": {
            "Authorization": "Bearer <jwt>"
       },
       "cookies": {
               "refresh_token": ""
           }
       },
        "body": {
   
       },
    }
    response = {
       "json": {
           "image": "",
           "is_main_image": ""
       }
    }
   6. Создаем фото профиля (анкеты):
   url = http://127.0.0.1:8000/api/profiles/images/add/
   method = POST
   media type = application/json
   content = {
       "headers": {
            "Authorization": "Bearer <jwt>"
       },
       "cookies": {
               "refresh_token": ""
           }
       },
        "body": {
           # Отправляем через form-data, и даем тип полю image file, так как туда будем загружать изображение
           "image": "",
           "is_main_image": ""
       },
    }
    response = {
       "json": {
           "image": "",
           "is_main_image": ""
       }
    } 
   7. Список фото профиля (анкеты):
   url = http://127.0.0.1:8000/api/profiles/images/
   method = GET
   media type = application/json
   content = {
       "headers": {
            "Authorization": "Bearer <jwt>"
       },
       "cookies": {
               "refresh_token": ""
           }
       },
        "body": {
       },
    }
    response = {
       "json": {
           [
               "image": "",
               "is_main_image": ""
           ]
       }
    } 
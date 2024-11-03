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

    4. Добавить бд в изображение postgres:
    docker-compose exec db sh
    psql -U postgres
    create database morfix_django_restapi;






Документация API:

1. Приложение - users:

   1. Регистрация:
   url = http://127.0.0.1:8000/api/user/register/
   method = POST
   media type = application/json
   content = {
       "username": "",
       "password": ""
   }
   response = {
       "json": {
           "access": ""
           "user": {
               "id": "",
               "username": "",
           }
       },
       cookies: {
               "refresh_token": ""
           }
       }
   }

   2. Авторизация:
   url = http://127.0.0.1:8000/api/user/login/
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
           }
       },
       cookies: {
               "refresh_token": ""
           }
       }
   }

   3. Обновление пользователя:
   url = http://127.0.0.1:8000/api/user/update/
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
       },
   }
   
   4. Данные пользователя:
   url = http://127.0.0.1:8000/api/user/
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
       },
   }
   5. Удаление пользователя:
   url = http://127.0.0.1:8000/api/user/delete/
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
        }
   }
   response = {
       "json": {
           "detail": "Ваш аккаунт был успешно удален."
       },
   }

   6. Генерация нового refresh токена:
   url = http://127.0.0.1:8000/api/user/token/refresh/
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
           "access": ""
       },
       "cookies": {
               "refresh_token": ""
           }
       }
   }
   7. Выход пользователя:
   url = http://127.0.0.1:8000/api/user/logout/
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
           "detail": "Ваш аккаунт был успешно удален."
       },
       "cookies": {
               "refresh_token": ""
           }
       }
   }



2. Приложение - profiles:

    1. Создание профиля (анкеты):
    url = http://127.0.0.1:8000/api/profile/create/
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
           "first_name": "", # Строка
           "gender": "", # Выбор одного из следующих значений: "RELATIONSHIP" (серьезные отношения), "FRIENDSHIP" (Общение и дружба), "FLIRT" (Флирт и свидания), "UNRESOLVED" (Решу потом)
           "birthday": "", # Дата в формате: YYYY-MM-DD
           "dating_purpose": "", # Выбор одного из следующих значений: "MALE" (Мужчина), "FEMALE" (Женщина)
           "searching_gender": "" # Выбор одного из следующих значений: "MALE" (Мужчина), "FEMALE" (Женщина)
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
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "age": "",
           "is_active": true/false,
       }
    } 
   2. Обновление профиля (анкеты):
   url = http://127.0.0.1:8000/api/profile/update/
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
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "age": "",
           "is_active": true/false,
       }
    } 
   3. Данные профиля (анкеты):
   url = http://127.0.0.1:8000/api/profile/
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
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "age": "",
           "is_active": true/false,
       }
    } 
   4. Данные профиля вместе с хобби и изображениями (анкеты):
   url = http://127.0.0.1:8000/api/profile/full-info/
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
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "age": "",
           "is_active": true/false,
           "hobbies": [],
           "images": []
       }
    } 
   5. Данные подходящих профилей (анкет):
   url = http://127.0.0.1:8000/api/profile/search-profiles/?profiles_count=<int>&allowed_age_difference=<int>
   profiles_count - количество запрашиваемых профилей - int
   allowed_age_difference - разрешенная разница в возрасте - int
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
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "age": "",
           "is_active": true/false,
           "hobbies": [],
           "images": []
       }
    } 
   6. Удаление фото профиля (анкеты):
   url = http://127.0.0.1:8000/api/profile/image/<id_фото>/delete/
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
   7. Обновление фото профиля (анкеты):
   url = http://127.0.0.1:8000/api/profile/image/<id_фото>/update/
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
            # Контент может иметь любые поля сущности
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
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "age": "",
           "is_active": true/false
       }
    } 
   7. Данные фото профиля (анкеты):
   url = http://127.0.0.1:8000/api/profile/image/<id_фото>/
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
   8. Создаем фото профиля (анкеты):
   url = http://127.0.0.1:8000/api/profile/image/add/
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
   9. Список фото профиля (анкеты):
   url = http://127.0.0.1:8000/api/profile/images/
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
   10. Добавление хобби профиля (анкеты):
   url = http://127.0.0.1:8000/api/profile/hobby/add/
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
           "name": ""
       },
    }
    response = {
       "json": {
           "id": "",
           "name": ""
       }
    } 
   11. Удаление хобби профиля (анкеты):
   url = http://127.0.0.1:8000/api/profile/hobby/<id_хобби>/delete/
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
           "detail": "Хобби профиля успешно удалено."
       }
    } 
   12. Все хобби профиля (анкеты):
   url = http://127.0.0.1:8000/api/profile/hobbies/
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
       "json": [
           {
               "id": "",
               "name": ""
           }
       ]
    } 
   13. Все cуществующие хобби в бд:
   url = http://127.0.0.1:8000/api/profile/hobbies-list/
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
       "json": [
           {
               "id": "",
               "name": ""
           }
       ]
    } 
   14. Добавление списка хобби:
   url = http://127.0.0.1:8000/api/profile/hobbies/add/
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
           [
               {
                   "name": "" # Имя хобби
               }
           ]
       },
    }
    response = {
       "json": [
           {
               "id": "",
               "name": ""
           }
       ]
    } 

   15. Добавление чата:
   url = http://127.0.0.1:8000/api/profile/create-chat/
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
            "profile_id": "" #id профиля
       },
    }
    response = {
       1. "json": {
            "detail": "Профиль не был создан." # Если анкеты текущего пользователя не существует
        }
       2. "json": {
            "detail": "Анкеты, которая понравилась, не существует." # Если анкеты, которую лайкают, не существует
        }
       3. "json": {
            "detail": "Чат успешно создан." # Если человек, который понравился, до этого уже лайкнул текущий профиль
        }
       4. "json": {
            "detail": "Лайк успешно создан." # Если текущий профиль впервые лайкнул понравившуюся анкету
        }
       5. "json": {
            "detail": "Лайк уже был отправлен." # Если текущий профиль уже лайкал понравившуюся анкету
        }
    } 

3. Приложение - chats:
   1. Все чаты пользователя:
   url = http://127.0.0.1:8000/api/chat/list/
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
       "json": [
            {
                "chat_id": 1,
                "other_profile_image": "/media/profiles/images/....jpg",
                "other_profile_first_name": "Vladislav",
                "last_message_first_name": "Вы",
                "last_message_text": "last message test",
                "last_message_datetime": "14:48",
                "unseen_messages_length": 0
            }
       ]
    }
   2. Комната чата пользователя:
   url = http://127.0.0.1:8000/api/chat/<chat_id>/
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
       "json": [
            {
                'id': "",
                'chat': "",
                'sender': "",
                'datetime': "",
                'text': "",
                'media': ""
            }
       ]
    }
   3. Websockets чатов:
   url = ws://127.0.0.1:8000/ws/chat/<chat_id>/
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
           "action": # Разрешенные значения: send, edit, delete
           "data": {
               "message_id": 1 # ID сообщения (данное поле используется только для действий: редактирование или удаление) 
               "text": "" # Текст сообщения (данное поле используется только для действий: отправка или редактирование)
               "media": "" # Медиа сообщения (данное поле используется только для действий: отправка или редактирование)
           }
       },
    }
    response = {
       "json": {
           "message": "", # Текст сообщения
           "media": "" # Медиа сообщения
       }
    }
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
   8. Обновление активности пользователя:
   url = http://127.0.0.1:8000/api/user/heartbeat/
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
           "detail": "Активность текущего пользователя успешно обновлена."
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
           "location": {
                "latitude": 53.196860, # double 
                "longitude": 50.158323 # double
            }
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
           "location": "SRID=4326;POINT (50.136764 53.113152)",
           "description": "",
           "smokes_cigarettes": "",
           "drinks_alcoholics": "",
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "address": "",
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
           "location": "SRID=4326;POINT (50.136764 53.113152)",
           "description": "",
           "smokes_cigarettes": "",
           "drinks_alcoholics": "",
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "address": "",
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
           "location": "SRID=4326;POINT (50.136764 53.113152)",
           "description": "",
           "smokes_cigarettes": "",
           "drinks_alcoholics": "",
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "address": "",
           "age": "",
           "is_active": true/false,
       }
    } 
   4. Данные профиля вместе с хобби и изображениями (анкеты):
   url = http://127.0.0.1:8000/api/profile/full-info/<id_profile>/
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
           "location": "SRID=4326;POINT (50.136764 53.113152)",
           "description": "",
           "smokes_cigarettes": "",
           "drinks_alcoholics": "",
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "address": "",
           "age": "",
           "is_active": true/false,
           "user_id": "",
           "username": "",
           "hobbies": [],
           "images": []
       }
    } 
   5. Данные текущего профиля вместе с хобби и изображениями (анкеты):
   url = http://127.0.0.1:8000/api/profile/full-info/me/
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
           "location": "SRID=4326;POINT (50.136764 53.113152)",
           "description": "",
           "smokes_cigarettes": "",
           "drinks_alcoholics": "",
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "address": "",
           "age": "",
           "is_active": true/false,
           "user_id": "",
           "username": "",
           "hobbies": [],
           "images": []
       }
    }
   6. Данные подходящих профилей (анкет):
   http://127.0.0.1:8000/api/profile/search-profiles/?radius=<int>&min_age=<int>&max_age=<int>
   raduis - радиус поиска анкет (int)
   min_age - минимальный возраст искомых анкет (int)
   max_age - максимальный возраст искомых анкет (int)
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
           "location": "SRID=4326;POINT (50.136764 53.113152)",
           "description": "",
           "smokes_cigarettes": "",
           "drinks_alcoholics": "",
           "has_children": "",
           "zodiac_signs": "",
           "education": "",
           "job": "",
           "address": "",
           "age": "",
           "is_active": true/false,
           "user_id": "",
           "username": "",
           "hobbies": [],
           "images": []
       }
    } 
   7. Удаление фото профиля (анкеты):
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
   8. Обновление фото профиля (анкеты):
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
   9. Данные фото профиля (анкеты):
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
   10. Создаем фото профиля (анкеты):
   url = http://127.0.0.1:8000/api/profile/images/add/
   method = POST
   media type = form-data
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
           ***Отправляем данные первого изображения профиля***
           "image_<photo_index>": "", # photo_index начинается с одного
           "is_main_image_<photo_index>": "" # photo_index начинается с одного
           photo_index++;
           ***Отправляем данные второго изображения профиля***
           "image_<photo_index>": "", # photo_index начинается с одного
           "is_main_image_<photo_index>": "" # photo_index начинается с одного
       },
    }
    response = {
       "json": {
           "image": "",
           "is_main_image": ""
       }
    } 
   11. Список фото профиля (анкеты):
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
   12. Добавление хобби профиля (анкеты):
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
   13. Удаление хобби профиля (анкеты):
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
   14. Все хобби профиля (анкеты):
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
   15. Все cуществующие хобби в бд:
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
   16. Добавление списка хобби:
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

   17. Создание лайка:
   url = http://127.0.0.1:8000/api/profile/like/create/
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
   18. Создание лайка:
   url = http://127.0.0.1:8000/api/profile/like/<like_id>/delete/
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
        "profile_id": "" #id профиля
   },
    }
    response = {
       1. "json": {
            "detail": "Лайк успешно удален."
          }
    } 
   19. Список лайков, отправленных текущему пользователю:
   url = http://127.0.0.1:8000/api/profile/likes/
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
        "profile_id": "" #id профиля
   },
    }
    response = {
       1. "json": [
          {
               "like": {
                   "id": "",
                   "type": "",
                   "receiver_id": "",
                   "sender_id": "",
               },
               "profile": {
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
                   "user_id": "",
                   "username": "",
                   "hobbies": [],
                   "images": []
               }
          }
       ]
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
                "profile_id": 2,
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
                'chat_id': "",
                'sender_id': "",
                'datetime': "",
                'text': "",
                'media': ""
            }
       ]
    }
   3. Удаление чата пользователя:
   url = http://127.0.0.1:8000/api/chat/<chat_id>/delete/
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
           "detail": "Чат успешно удален."
       }
    }
   4. Маршрут активности пользователей-собеседников чатов:
   url = http://127.0.0.1:8000/api/chat/users-activity/
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
                "chat_id": 4,
                "other_user_is_online": true,
                "other_user_last_activity": ""
            }
       ]
    }
   5. Websocket чата:
   url = ws://127.0.0.1:8000/ws/chat/<chat_id>/?token=<access_token>
   media type = application/json
   content = {
        "body": {
                 ***Отправка сообщения***
                 {
                        "action": "send",
                        "data": {
                            "text": "",
                            "media": null
                        }
                 }
                 ***Редактирование сообщения***
                 {
                        "action": "edit",
                        "data": {
                            "message_id": 0,
                            "text": "",
                            "media": null
                        }
                 }
                 ***Удаление сообщения***
                 {
                        "action": "delete",
                        "data": {
                            "message_id": 0
                        }
                 }
       },
    }
    response = {
       "json": {
                 ***Отправка сообщения***
                 {
                     "action": "send",
                     "message": {
                         "id": 0,
                         "chat_id": 0,
                         "sender_id": 0,
                         "datetime": "2024-11-08T12:14:38.649364Z",
                         "text": "",
                         "media": null
                     }
                 }
                 ***Редактирование сообщения***
                 {
                     "action": "edit",
                     "message": {
                         "id": 0,
                         "chat_id": 0,
                         "sender_id": 0,
                         "datetime": "2024-11-08T12:14:20.028332Z",
                         "text": "",
                         "media": null
                     }
                 }
                 ***Удаление сообщения***
                 {
                        {
                             "action": "delete",
                             "message_id": 19
                         }
                 }
       }
    }
   6. Websocket списка чатов:
   url = ws://127.0.0.1:8000/ws/chats/?token=<access_token>
   media type = application/json
   content = {
        "body": {
       },
    }
    response = {
       "json": { 
   ***При отправке сообщения***
   {
     "type": "send.event.update",
     "chat_id": 0,
     "last_message_first_name": "" , # Если отправитель сообщения это текущий пользователь, тогда будет значение "Вы"
     "last_message_text": "",
     "last_message_datetime": "2024-11-08T12:31:28.914479+00:00",
     "unseen_messages_length": 0 
   }
   ***Когда был не в чате, а потом зашел в него***
   {
     "type": "send.event.update",
     "chat_id": 0,
     "unseen_messages_length": 0 
   }

**Полученя активности пользователей-собеседников чатов**

   {
    "type": "send.active.users",
    "chats_users_activity": [
        {
            "chat_id": 1,
            "other_user_is_online": true,
            "other_user_last_activity": "2024-11-20T19:12:16.937787+00:00"
        }
    ]
}
       }
    }
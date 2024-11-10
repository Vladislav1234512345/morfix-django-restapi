# from django.db import models
from django.contrib.gis.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None

    last_activity = models.DateTimeField(verbose_name="Последняя активность", auto_now=True)
    is_online = models.BooleanField(verbose_name="Пользователь онлайн", default=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

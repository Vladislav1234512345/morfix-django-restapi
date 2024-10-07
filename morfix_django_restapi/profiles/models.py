from tabnanny import verbose

from django.db import models
from users.models import User

from datetime import date

# Create your models here.

class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Мужчина'
        FEMALE = 'FEMALE', 'Женщина'

    class ZodiacSigns(models.TextChoices):
        ARIES = 'ARIES', 'Овен'
        TAURUS = 'TAURUS', 'Телец'
        GEMINI = 'GEMINI', 'Близнецы'
        CANCER = 'CANCER', 'Рак'
        LEO = 'LEO', 'Лев'
        VIRGO = 'VIRGO', 'Девы'
        LIBRA = 'LIBRA', 'Весы'
        SCORPIO = 'SCORPIO', 'Скорпион'
        SAGITTARIUS = 'SAGITTARIUS', 'Стрелец'
        CAPRICORN = 'CAPRICORN', 'Козерог'
        AQUARIUS = 'AQUARIUS', 'Водолей'
        PISCES = 'PISCES', 'Рыбы'

    class DatingPurpose(models.TextChoices):
        RELATIONSHIP = 'RELATIONSHIP', 'Серьезные отношения'
        FRIENDSHIP = 'FRIENDSHIP', 'Общение и дружба'
        FLIRT = 'FLIRT', 'Флирт и свидания'
        UNRESOLVED = 'UNRESOLVED', 'Решу потом'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='Имя пользователя', max_length=200)
    last_name = models.CharField(verbose_name='Фамилия пользователя', max_length=200)
    gender = models.CharField(verbose_name='Пол', choices=Gender.choices, max_length=6, null=False, blank=False)
    birthday = models.DateField(verbose_name='День рождения', null=False, blank=False)
    dating_purpose = models.CharField(verbose_name='Цель знакомства', choices=DatingPurpose.choices, max_length=12, null=False, blank=False)
    description = models.TextField(verbose_name='О себе', max_length=5000, null=True, blank=True)
    searching_gender = models.CharField(verbose_name='Кого ищет', choices=Gender.choices, max_length=6, null=False, blank=False)
    smokes_cigarettes = models.BooleanField(verbose_name='Курит сигареты', null=True, blank=True)
    drinks_alcoholics = models.BooleanField(verbose_name='Пьёт алкоголь', null=True, blank=True)
    zodiac_signs = models.BooleanField(verbose_name='Знаки Зодиака', choices=ZodiacSigns.choices, max_length=11, null=True, blank=True)
    education = models.CharField(verbose_name='Обучение', max_length=200, null=True, blank=True)
    job = models.CharField(verbose_name='Работа', max_length=200, null=True, blank=True)

    @property
    def age(self):
        today = date.today()

        age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return age


    class Meta:
        db_table = 'profiles'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class ProfileImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение', upload_to='profiles/images/', null=False)
    uploaded_at = models.DateTimeField(verbose_name='Дата загрузки', auto_now_add=True)
    is_main_image = models.BooleanField(verbose_name='Изображение профиля', default=False)

    class Meta:
        db_table = 'profile_images'
        verbose_name = 'Изображение профиля'
        verbose_name_plural = 'Изображения профиля'

# Generated by Django 5.1.1 on 2024-10-06 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(max_length=200, verbose_name='Фамилия пользователя')),
                ('gender', models.CharField(choices=[('MALE', 'Мужчина'), ('FEMALE', 'Женщина')], max_length=6, verbose_name='Пол')),
                ('birthday', models.DateField(verbose_name='День рождения')),
                ('dating_purpose', models.CharField(choices=[('RELATIONSHIP', 'Серьезные отношения'), ('FRIENDSHIP', 'Общение и дружба'), ('FLIRT', 'Флирт и свидания'), ('UNRESOLVED', 'Решу потом')], max_length=12, verbose_name='Цель знакомства')),
                ('description', models.TextField(blank=True, max_length=5000, null=True, verbose_name='О себе')),
                ('searching_gender', models.CharField(choices=[('MALE', 'Мужчина'), ('FEMALE', 'Женщина')], max_length=6, verbose_name='Кого ищет')),
                ('smokes_cigarettes', models.BooleanField(blank=True, null=True, verbose_name='Курит сигареты')),
                ('drinks_alcoholics', models.BooleanField(blank=True, null=True, verbose_name='Пьёт алкоголь')),
                ('zodiac_signs', models.BooleanField(blank=True, choices=[('ARIES', 'Овен'), ('TAURUS', 'Телец'), ('GEMINI', 'Близнецы'), ('CANCER', 'Рак'), ('LEO', 'Лев'), ('VIRGO', 'Девы'), ('LIBRA', 'Весы'), ('SCORPIO', 'Скорпион'), ('SAGITTARIUS', 'Стрелец'), ('CAPRICORN', 'Козерог'), ('AQUARIUS', 'Водолей'), ('PISCES', 'Рыбы')], max_length=11, null=True, verbose_name='Знаки Зодиака')),
                ('education', models.CharField(blank=True, max_length=200, null=True, verbose_name='Обучение')),
                ('job', models.CharField(blank=True, max_length=200, null=True, verbose_name='Работа')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
                'db_table': 'profiles',
            },
        ),
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='profiles/images/', verbose_name='Изображение')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')),
                ('is_profile_image', models.BooleanField(default=False, verbose_name='Изображение профиля')),
            ],
            options={
                'verbose_name': 'Изображение профиля',
                'verbose_name_plural': 'Изображения профиля',
                'db_table': 'profile_images',
            },
        ),
    ]
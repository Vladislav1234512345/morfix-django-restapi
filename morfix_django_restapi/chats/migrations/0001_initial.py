# Generated by Django 5.1.1 on 2024-11-09 23:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя чата')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение чата')),
                ('is_group', models.BooleanField(default=False, verbose_name='Чат является группой')),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Чаты',
                'db_table': 'chats',
            },
        ),
        migrations.CreateModel(
            name='ChatUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('invite_reason', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Пользователь чата',
                'verbose_name_plural': 'Пользователи чата',
                'db_table': 'chat_users',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(max_length=5000)),
                ('media', models.FileField(blank=True, null=True, upload_to='chat_media/')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'db_table': 'messages',
            },
        ),
        migrations.CreateModel(
            name='ChatEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_events', to='chats.chat')),
            ],
            options={
                'verbose_name': 'Событие чата',
                'verbose_name_plural': 'События чата',
                'db_table': 'chat_events',
            },
        ),
    ]

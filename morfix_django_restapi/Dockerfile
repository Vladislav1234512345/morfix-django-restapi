# Используем базовый образ Python
FROM python:3.11-alpine3.18

# Устанавливаем postgresql-client через apk
RUN apk update && apk add --no-cache postgresql-client

# Устанавливаем зависимости для PostgreSQL и пакеты для работы с геоданными
RUN apk update && apk add --no-cache --virtual .build-deps \
    postgresql-dev \
    gcc \
    musl-dev \
    libffi-dev \
    gdal-dev \
    geos-dev \
    proj-dev \
    proj-util \
    sfcgal-dev && \
    apk add --no-cache \
    geos \
    proj \
    gdal

## Установка зависимостей для PostgreSQL и других пакетов
#RUN apk add --no-cache postgresql-dev gcc musl-dev libffi-dev

# Устанавливаем переменные окружения для GDAL и PROJ
ENV GDAL_DATA=/usr/share/gdal
ENV PROJ_LIB=/usr/share/proj

# Рабочая директория
WORKDIR /usr/src/app

# Создание директорий для статических и медиафайлов
RUN mkdir -p static media

# Переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Обновим pip
RUN pip install --upgrade pip

# Скопируем файл с зависимостями и установим их
COPY ./requirements.txt ./
RUN pip install -r requirements.txt --verbose


# Скопируем оставшиеся файлы проекта
COPY . .

# Проверка наличия manage.py
RUN ls -la /usr/src/app/

RUN python3 manage.py collectstatic --noinput

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

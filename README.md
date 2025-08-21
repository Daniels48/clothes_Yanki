<h1 align="center">Yanki Django Project</h1>

## Описание

Проект на Django с использованием PostgreSQL. Можно запускать локально через `runserver` или через Docker. Все медиа-файлы и база данных остаются в контейнерах при использовании Docker, что упрощает переносимость и настройку окружения.

## Требования

- Python 3.11+  
- Django 4+  
- PostgreSQL 15  
- Docker и Docker Compose (если планируется запуск в контейнерах)  

## Установка и запуск

Скопируйте `.env.example` в тот же каталог с именем `.env` и заполните свои данные:

```bash
cp ./.env.example ./.env

Для запуска через Docker соберите и запустите контейнеры: docker-compose up -d --build. 
Сайт будет доступен по адресу http://localhost:8000/.

Для локального запуска через runserver установите зависимости: pip install -r requirements.txt. 
Используется локальная база SQLite (db.sqlite3). 
Если нужно, создайте миграции: python manage.py migrate. 
Запустите сервер разработки: python manage.py runserver. 
Сайт будет доступен по адресу http://127.0.0.1:8000/.
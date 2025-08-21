FROM python:3.11-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    libpq-dev gcc netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Делаем wait-for-db исполняемым
RUN chmod +x /app/wait-for-db.sh

# Запуск через wait-for-db
CMD ["./wait-for-db.sh", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

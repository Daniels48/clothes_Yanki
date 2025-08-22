#!/bin/sh

# Скрипт ждет готовности PostgreSQL перед запуском приложения Django

echo "⏳ Waiting for Postgres at $DBHost:$DBPort..."

# Ждем, пока БД не станет готовой к приему подключений
until pg_isready -h "$DBHost" -p "$DBPort" -U "$DBUser" > /dev/null 2>&1; do
  echo "⏳ Postgres is not ready yet..."
  sleep 1
done

echo "✅ Postgres is up! Starting the application..."

# Запуск команды, переданной в Dockerfile или docker-compose
exec "$@"

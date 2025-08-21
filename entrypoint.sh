#!/bin/sh

echo "⏳ Waiting for Postgres at $DBHost:$DBPort..."

while ! nc -z $DBHost $DBPort; do
  sleep 1
done

echo "✅ Postgres is up!"

exec "$@"

#!/bin/sh
echo "Waiting for postgres..."

while ! netcat -z db 5432; do
  sleep 0.1
done

echo "Running migrations"
python manage.py migrate

exec "$@"

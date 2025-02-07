#!/bin/sh
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
gunicorn url_shortener.wsgi:application --bind 0.0.0.0:8000

#!/bin/sh
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Checking if superuser exists, create if not..."
    python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    print("Creating superuser...")
    User.objects.create_superuser("${DJANGO_SUPERUSER_USERNAME}", "${DJANGO_SUPERUSER_EMAIL}", "${DJANGO_SUPERUSER_PASSWORD}")
else:
    print("Superuser already exists.")
EOF
else
    echo "Skipping superuser creation..."
fi

echo "Starting Gunicorn..."
gunicorn url_shortener.wsgi:application --bind 0.0.0.0:8000

#!/bin/sh
echo "Starting application..."

python manage.py migrate --noinput

if [ "$DJANGO_ENV" = "production" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
    echo "Running Gunicorn..."
    # Default Gunicorn timeout is 30s; large Wagtail/media uploads exceed it (WORKER TIMEOUT).
    # Override on the host if needed, e.g. GUNICORN_TIMEOUT=3600 docker compose up -d
    GUNICORN_TIMEOUT="${GUNICORN_TIMEOUT:-1200}"
    exec gunicorn ruzivoflow.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout "$GUNICORN_TIMEOUT" \
        --graceful-timeout 120
else
    echo "Running Django dev server..."
    exec python manage.py runserver 0.0.0.0:8000
fi

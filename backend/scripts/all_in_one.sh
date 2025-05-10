#!/usr/bin/env sh

set -e
echo "Starting background celery..."
poetry run celery -A backend.project worker -l INFO &

echo "Running migrations..."
poetry run python -m backend.manage migrate --no-input

echo "Running daphne on port 80..."
poetry run daphne -b 0.0.0.0 -p 80 backend.project.asgi:application

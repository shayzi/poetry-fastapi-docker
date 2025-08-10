#!/bin/bash
set -e

echo "Starting FastAPI application..."

# Only run migrations if we have a database URL configured
if cd /app && PYTHONPATH=./app poetry run python -c "from config import settings; print(getattr(settings, 'database_url', 'NOT_SET'))" | grep -v "NOT_SET" > /dev/null 2>&1; then
    echo "Database URL found, running migrations..."
    PYTHONPATH=./app poetry run alembic upgrade head
else
    echo "No database URL configured, skipping migrations..."
fi

echo "Starting application..."
cd /app/app && exec poetry run python main.py

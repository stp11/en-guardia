#!/bin/sh
set -e

echo "Starting application on port $PORT"

echo "Running database migrations..."
alembic upgrade head
echo "Migrations complete."

# Start uvicorn
echo "Starting uvicorn..."
exec uvicorn main:app --host :: --port ${PORT:-8080}

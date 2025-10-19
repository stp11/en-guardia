#!/bin/sh
set -e

cd /app

# Railway provides PGHOST/PGPORT, which are standard Postgres env vars
if [ -n "$PGHOST" ] && [ -n "$PGPORT" ]; then
  echo "Waiting for Postgres at $PGHOST:$PGPORT..."
  while ! nc -z "$PGHOST" "$PGPORT"; do
    echo "Postgres not ready, sleeping 1s..."
    sleep 1
  done
  echo "Postgres is ready!"
else
  echo "Warning: Postgres host not configured, skipping health check"
fi

# Extract Redis host and port from REDIS_URL (format: redis://host:port/db)
if [ -n "$REDIS_URL" ]; then
  REDIS_HOSTPORT=$(echo "$REDIS_URL" | sed 's|redis://||' | sed 's|.*@||' | sed 's|/.*||')
  REDIS_HOST=$(echo "$REDIS_HOSTPORT" | cut -d: -f1)
  REDIS_PORT=$(echo "$REDIS_HOSTPORT" | cut -d: -f2)

  if [ -n "$REDIS_HOST" ] && [ -n "$REDIS_PORT" ]; then
    echo "Waiting for Redis at $REDIS_HOST:$REDIS_PORT..."
    while ! nc -z "$REDIS_HOST" "$REDIS_PORT"; do
      echo "Redis not ready, sleeping 1s..."
      sleep 1
    done
    echo "Redis is ready!"
  fi
else
  echo "Warning: REDIS_URL not configured, skipping health check"
fi

echo "Starting Celery worker..."
exec celery -A tasks.main worker --concurrency=1 --loglevel=info

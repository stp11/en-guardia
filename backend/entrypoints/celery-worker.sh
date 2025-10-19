#!/bin/sh
set -e

echo "Starting Celery worker..."
exec celery -A tasks.main worker --concurrency=1 --loglevel=info

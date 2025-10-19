#!/bin/sh
set -e

echo "Starting Celery beat scheduler..."
exec celery -A tasks.main beat --loglevel=info

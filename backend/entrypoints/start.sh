#!/bin/sh
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting uvicorn on port ${PORT:-8080}..."
if [ "$BUILD_ENVIRONMENT" = "local" ]; then
    exec uvicorn main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8080} --reload
fi
exec uvicorn main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8080} --proxy-headers

#!/bin/sh
set -e

RUN_MIGRATIONS_NORMALIZED=$(printf '%s' "${RUN_MIGRATIONS:-true}" | tr '[:upper:]' '[:lower:]')
if [ "$RUN_MIGRATIONS_NORMALIZED" = "true" ]; then
  echo ">>> Running database migrations..."
  python manage.py migrate --noinput
else
  echo ">>> Skipping database migrations (RUN_MIGRATIONS=${RUN_MIGRATIONS:-false})"
fi

# Collect static files in production (DEBUG=False)
DEBUG_NORMALIZED=$(printf '%s' "$DEBUG" | tr '[:upper:]' '[:lower:]')
if [ "$DEBUG_NORMALIZED" != "true" ]; then
  echo ">>> Collecting static files..."
  python manage.py collectstatic --noinput --clear
fi

echo ">>> Starting application..."
exec "$@"

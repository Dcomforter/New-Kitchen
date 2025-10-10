#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate

echo "Loading initial data..."
if [ -f all_data.json ]; then
  python manage.py loaddata all_data.json || echo "Warning: loaddata failed"
else
  echo "No all_data.json found, skipping"
fi

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000

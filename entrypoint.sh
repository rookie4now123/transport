#!/bin/sh
# entrypoint.sh

# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

# Run migrations and start server
python manage.py migrate
exec "$@"
#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; do
    sleep 1
done
echo "PostgreSQL is ready."

echo "Running migrations..."
python /app/data/migrate.py

echo "Starting Flask application (auto-initializes corpus + auto-summaries)..."
python /app/app.py &
APP_PID=$!

wait $APP_PID
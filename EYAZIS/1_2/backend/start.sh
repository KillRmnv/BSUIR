#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; do
    sleep 1
done
echo "PostgreSQL is ready."

echo "Running migrations..."
python /app/migrate.py

echo "Starting Flask application..."
python /app/app.py &
APP_PID=$!

echo "Waiting for Flask to be ready..."
READY=0
for i in $(seq 1 60); do
    if python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/stats', timeout=2)" > /dev/null 2>&1; then
        READY=1
        break
    fi
    sleep 1
done

if [ "$READY" -ne 1 ]; then
    echo "ERROR: Flask did not become ready in time." >&2
    exit 1
fi
echo "Flask is ready."

echo "Loading corpus documents..."
DOC_COUNT=$(python -c "
import urllib.request, json
try:
    resp = json.load(urllib.request.urlopen('http://localhost:5000/api/stats', timeout=5))
    print(resp.get('document_count', 0))
except Exception:
    print(0)
")

if [ "$DOC_COUNT" -eq 0 ] 2>/dev/null; then
    python -c "
import urllib.request
req = urllib.request.Request('http://localhost:5000/api/init-db', method='POST')
print(urllib.request.urlopen(req, timeout=120).read().decode())
"
else
    echo "Corpus already loaded ($DOC_COUNT documents). Skipping."
fi

wait $APP_PID
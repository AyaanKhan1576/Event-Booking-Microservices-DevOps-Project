#!/bin/sh
set -e

echo "Waiting for Postgres to be available..."

# Wait until Postgres is available
while ! pg_isready -h postgres -p 5432 -U postgres; do
  sleep 2
done

echo "Postgres is available. Starting the FastAPI application..."

exec uvicorn main:app --reload --host 0.0.0.0 --port 8000

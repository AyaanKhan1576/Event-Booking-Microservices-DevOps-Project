#!/bin/sh
set -e  # Exit on error

# Ensure migrations exist
if [ ! -d "migrations/versions" ]; then
    flask db init --directory migrations
fi

flask db migrate --directory migrations -m "Auto migration"
flask db upgrade --directory migrations

# Start the Flask app
exec flask run --host=0.0.0.0 --port=5001

# #!/bin/sh
# set -e  # Exit on error

# # Ensure migrations exist
# if [ ! -d "migrations/versions" ]; then
#     flask db init --directory migrations
# fi

# flask db migrate --directory migrations -m "Auto migration"
# flask db upgrade --directory migrations

# # Start the Flask app
# exec flask run --host=0.0.0.0 --port=5001

#!/bin/sh
set -e  # Exit on error

# Remove old migrations directory if it exists
if [ -d "migrations" ]; then
    echo "Removing old migrations..."
    rm -rf migrations
fi

# Reinitialize migrations
echo "Initializing new migrations..."
flask db init --directory migrations

# Generate a new migration
echo "Generating new migration..."
flask db migrate --directory migrations -m "Auto migration"

# Apply migrations to the database
echo "Applying migrations..."
flask db upgrade --directory migrations

# Start the Flask app
exec flask run --host=0.0.0.0 --port=5001

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

echo "Waiting for Postgres to be ready..."
while ! pg_isready -h postgres -p 5432 -U postgres; do
    sleep 2
done
echo "Postgres is ready."

# Drop the alembic_version table from the database
echo "Dropping alembic_version table if exists..."
psql "$DATABASE_URL" -c "DROP TABLE IF EXISTS alembic_version;" || echo "Could not drop alembic_version table, proceeding anyway."

# Remove old migrations 
echo "Removing old migrations directory..."
rm -rf migrations

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

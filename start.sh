#!/bin/bash
set -ex

# Ensure DATABASE_URL is in the correct format for Python/SQLAlchemy
if [[ $DATABASE_URL == postgres://* ]]; then
  export DATABASE_URL="${DATABASE_URL/postgres:\/\//postgresql:\/\/}"
fi

cat <<EOF > alembic.ini
[alembic]
script_location = migrations
prepend_sys_path = .
sqlalchemy.url = $DATABASE_URL

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
EOF

echo "--- DEPLOYMENT STARTUP ---"

# Use pg_isready to wait for the database
echo "Waiting for database to be ready..."
for i in {1..30}; do
  if pg_isready -d "$DATABASE_URL"; then
    echo "Database is reachable!"
    break
  fi
  echo "Database not ready yet ($i/30)..."
  sleep 2
done

echo "Running migrations..."
alembic -c alembic.ini upgrade head || echo "Migration warning: proceeding anyway"

echo "Applying enum fixes..."
python fix_enums.py || echo "Enum fix warning: proceeding anyway"

echo "Seeding database..."
python seed.py || echo "Seeding warning: proceeding anyway"

echo "Finalizing startup on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

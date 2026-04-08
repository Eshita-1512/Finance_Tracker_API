#!/bin/bash
set -e


cat <<EOF > alembic.ini
[alembic]
script_location = migrations
prepend_sys_path = .
sqlalchemy.url = postgresql://user:pass@localhost/dbname

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

echo "Running database migrations..."
alembic -c alembic.ini upgrade head

echo "Fixing enum values..."
python fix_enums.py

echo "Seeding the database..."
python seed.py

echo "Starting the application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

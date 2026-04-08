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

echo "Waiting for database to be ready..."
python -c "
import os, time, sqlalchemy
from dotenv import load_dotenv
load_dotenv()
url = os.getenv('DATABASE_URL')
if url and url.startswith('postgres://'): url = url.replace('postgres://', 'postgresql://', 1)
engine = sqlalchemy.create_engine(url)
for i in range(30):
    try:
        engine.connect()
        print('Database is ready!')
        break
    except Exception as e:
        print(f'Waiting for database... ({i+1}/30)')
        time.sleep(2)
"

echo "Running database migrations..."
alembic -c alembic.ini upgrade head

echo "Fixing enum values..."
python fix_enums.py

echo "Seeding the database..."
python seed.py

echo "Starting the application on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

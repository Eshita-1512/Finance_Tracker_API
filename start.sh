#!/bin/bash

echo "Running database migrations..."
alembic upgrade head

echo "Seeding the database..."
python seed.py

echo "Starting the application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

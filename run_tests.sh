#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Starting test database..."
docker-compose -f docker-compose.test.yml up -d test-db

sleep 10

echo "Running tests..."
export TEST_DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5434/qa_test"
python -m pytest tests/ -v

echo "Stopping test database..."
docker-compose -f docker-compose.test.yml down
#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "========================================"
echo "Deep Work Session Tracker Setup"
echo "========================================"
echo

echo "[1/5] Creating Python virtual environment..."
cd backend
python3 -m venv env
source env/bin/activate

echo "[2/5] Installing Python dependencies..."
pip install -r requirements.txt

echo "[3/5] Running database migrations..."
alembic upgrade head

echo "[4/5] Seeding sample data..."
sqlite3 deepwork.db < seed_data.sql

echo "[5/5] Installing frontend dependencies..."
cd ../frontend
npm install

cd ..
echo
echo "========================================"
echo "Setup complete!"
echo "Run './run.sh' to start the app"
echo "========================================"

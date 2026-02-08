#!/bin/bash
cd "$(dirname "$0")"

echo "Starting Deep Work Session Tracker..."
echo

# start backend
echo "[Backend] Starting FastAPI server..."
cd backend
source env/bin/activate
uvicorn main:app --reload &
BACKEND_PID=$!

sleep 2

# start frontend
echo "[Frontend] Starting Vite dev server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo
echo "========================================"
echo "App is running!"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo "========================================"
echo "Press Ctrl+C to stop both servers"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait

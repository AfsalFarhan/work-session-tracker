@echo off
cd /d %~dp0

echo Starting Deep Work Session Tracker...
echo.

echo [Backend] Starting FastAPI server...
start cmd /k "cd backend && call env\Scripts\activate.bat && uvicorn main:app --reload"

timeout /t 3 /nobreak > nul

echo [Frontend] Starting Vite dev server...
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo App is starting up!
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo ========================================

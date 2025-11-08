@echo off
setlocal

echo Starting College Assistant Development Environment
echo ==================================================

REM Check if we're in the right directory
if not exist "backend" (
    echo Error: Please run this script from the website/ directory
    pause
    exit /b 1
)
if not exist "frontend" (
    echo Error: Please run this script from the website/ directory
    pause
    exit /b 1
)

echo Starting Flask Backend (Port 5000)...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate
pip install -r requirements.txt >nul 2>&1

REM Start Flask in background
echo ✓ Starting Flask server...
start "Flask Backend" cmd /c "python app.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting Next.js Frontend (Port 3000)...
cd ..\frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing npm dependencies...
    npm install
)

REM Start Next.js
echo ✓ Starting Next.js development server...
start "Next.js Frontend" cmd /c "npm run dev"

echo.
echo Development servers started successfully!
echo =========================================
echo 📡 Backend API: http://localhost:5000
echo 🌐 Frontend UI: http://localhost:3000
echo.
echo Press any key to stop servers and exit...
pause >nul

REM Kill the background processes (best effort)
taskkill /f /im "python.exe" >nul 2>&1
taskkill /f /im "node.exe" >nul 2>&1

echo ✓ Servers stopped. Thanks!

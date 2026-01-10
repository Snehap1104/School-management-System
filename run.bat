@echo off
echo ========================================
echo School Management System
echo Starting Application...
echo ========================================
echo.

REM Check if Python is available
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
py -m pip show Flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    py -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [2/3] Creating upload directories...
if not exist "uploads\student_photos" mkdir uploads\student_photos
if not exist "uploads\notes" mkdir uploads\notes

echo [3/3] Starting Flask application...
echo.
echo ========================================
echo Application is starting...
echo Access at: http://localhost:5000
echo Default Login: admin / admin123
echo Press CTRL+C to stop
echo ========================================
echo.

py app.py

pause

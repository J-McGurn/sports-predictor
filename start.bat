@echo off
title Sports Predictor Launcher

echo ========================================
echo          SPORTS PREDICTOR
echo ========================================
echo.

if not exist "%~dp0backend\venv\Scripts\activate.bat" (
    echo [ERROR] Backend virtual environment not found.
    echo Expected:
    echo %~dp0backend\venv\
    echo.
    pause
    exit /b 1
)

if not exist "%~dp0frontend\package.json" (
    echo [ERROR] Frontend package.json not found.
    echo.
    pause
    exit /b 1
)

echo [1/3] Starting Flask backend...
start "Sports Predictor - Backend" cmd /k "cd /d "%~dp0backend" && echo Activating virtual environment... && call venv\Scripts\activate.bat && echo Starting Flask... && python app.py"

echo.
echo [2/3] Starting React frontend...
start "Sports Predictor - Frontend" cmd /k "cd /d "%~dp0frontend" && echo Starting Vite... && npm run dev"

echo.
echo [3/3] Waiting for servers...
timeout /t 5 /nobreak > nul

echo.
echo Opening Sports Predictor...
start "" "http://localhost:5173"

echo.
echo ========================================
echo          SPORTS PREDICTOR STARTED
echo ========================================
echo.
echo Backend:  http://127.0.0.1:5000
echo Frontend: http://localhost:5173
echo.
pause
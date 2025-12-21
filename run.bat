@echo off
REM Crystal Agent - Simple Startup Script for Windows

echo ============================================================
echo 🔮 Crystal Agent - Starting Server...
echo ============================================================

REM Check if dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt --quiet
)

echo.
echo ✨ Starting FastAPI server...
echo 🌐 Open http://localhost:8000 in your browser
echo.

python backend\main.py

pause

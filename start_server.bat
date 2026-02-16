@echo off
echo ========================================
echo   DEEPFAKE DETECTOR - LOCAL SERVER
echo ========================================
echo.
echo Starting local development server...
echo Server will run at: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd /d "%~dp0"
python -m uvicorn api.index:app --host 127.0.0.1 --port 8000 --reload

pause

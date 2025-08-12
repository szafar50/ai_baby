@echo off
echo ==============================================
echo   Stopping any running Ollama process...
echo ==============================================
taskkill /F /IM ollama.exe >nul 2>&1

echo.
echo ==============================================
echo   Starting Ollama server...
echo ==============================================
start "" powershell -NoExit -Command "cd 'C:\Users\Admin\AppData\Local\Programs\Ollama'; .\ollama.exe serve"

echo.
echo Waiting 5 seconds for Ollama to warm up...
timeout /t 5 /nobreak >nul

echo.
echo ==============================================
echo   Starting FastAPI backend...
echo ==============================================
cd backend\src
uvicorn main:app --reload --port 8000

pause

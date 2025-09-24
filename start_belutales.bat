@echo off
echo ==================================================
echo   BeluTales One-Click Launcher
echo ==================================================

echo Checking for old processes on ports 8000 and 8502...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8502') do taskkill /PID %%a /F >nul 2>&1

echo Starting BeluTales Backend (Uvicorn) on port 8000...
start cmd /k "cd %USERPROFILE%\Documents\belutales && uvicorn server:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 5 >nul

echo Starting BeluTales Frontend (Streamlit) on port 8502...
start cmd /k "cd %USERPROFILE%\Documents\belutales && streamlit run app.py --server.port=8502"

timeout /t 3 >nul

echo Opening BeluTales in your default browser...
start http://localhost:8502

echo ==================================================
echo   BeluTales is now running!
echo   Backend: http://localhost:8000/docs
echo   Frontend: http://localhost:8502
echo ==================================================
pause

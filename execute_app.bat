echo ==========================================
echo      STARTING PROMPTWISE FULL APP
echo ==========================================

:: Start Backend in a new window
echo Starting Backend Server...
start "PromptWise Backend" cmd /k "venv\Scripts\python run_backend.py"

:: Wait a few seconds for backend to initialize
timeout /t 5 /nobreak >nul

:: Start Frontend in a new window
echo Starting Frontend UI...
cd promptwise-ui
start "PromptWise Frontend" cmd /k "npm run dev"

:: Open Browser
echo Opening App in Browser...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo ==========================================
echo    ✅ SYSTEM RUNNING
echo    Backend: http://127.0.0.1:8000
echo    Frontend: http://localhost:5173
echo ==========================================
pause

@echo off
title CivicGuide AI - Launcher
echo =======================================================
echo  Launching CivicGuide AI (Backend + Frontend)
echo  All India - Central & State Governments
echo =======================================================
cd /d "%~dp0"

echo Starting Backend Server in a new window...
start "CivicGuide AI Backend" cmd /k "python backend\run.py"

echo Waiting 3 seconds for Backend to initialize...
timeout /t 3 /nobreak > nul

echo Starting Frontend Server in a new window...
start "CivicGuide AI Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo =======================================================
echo  Both servers started!
echo  Backend:  http://127.0.0.1:5000
echo  Frontend: http://localhost:5173
echo =======================================================
pause

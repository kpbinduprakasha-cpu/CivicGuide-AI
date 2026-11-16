@echo off
title CivicGuide AI - Flask Backend
echo =======================================================
echo  Starting CivicGuide AI Flask Backend on port 5000...
echo =======================================================
cd /d "%~dp0"
python backend\run.py
pause

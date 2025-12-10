@echo off
cd /d %~dp0
call python -m uvicorn app.main:app --reload
pause

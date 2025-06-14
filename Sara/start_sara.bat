@echo off
cd /d %~dp0
start cmd /k "uvicorn backend:app --port 8001 --reload"
timeout /t 2
start python frontend.py
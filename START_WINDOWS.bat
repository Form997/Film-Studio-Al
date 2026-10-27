@echo off
cd /d "%~dp0"
where python >nul 2>nul || (echo Can cai Python 3.11+ & pause & exit /b 1)
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m studio
pause

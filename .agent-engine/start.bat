@echo off
REM Vibing Agent Engine Launcher (Windows)
REM This script starts the autonomous agent engine in a new PowerShell window

echo ===================================================================
echo   Vibing Agent Engine - Starting...
echo ===================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.9 or higher
    pause
    exit /b 1
)

REM Launch in new PowerShell window for better interactivity
start "Vibing Agent Engine" powershell -NoExit -Command "python '%~dp0launcher.py'"

echo.
echo Agent Engine launched in new window
echo.
pause

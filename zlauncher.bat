@echo off
title Ambibot

REM Change to the directory where the batch file is located
cd /d "%~dp0"

REM Run check_for_updates.bat (it will handle the config check internally)
call "%~dp0check_for_updates.bat"

REM Display ASCII art
if exist "ascii.txt" (
    type "ascii.txt"
) else (
    echo ascii.txt not found.
)

REM Run the Python script using the virtual environment's Python interpreter
"%~dp0venv\Scripts\python.exe" "%~dp0main.py"
if %errorlevel% neq 0 (
    echo Failed to run Python script.
    pause
    exit /b 1
)

REM Pause to keep the window open
pause
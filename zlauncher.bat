@echo off
title Ambibot
setlocal enabledelayedexpansion

:: Change to the script's directory
cd /d "%~dp0"

:: Display ASCII art
type "ascii.txt"

:: Check for updates
"%~dp0venv\Scripts\python.exe" -c "import settings; print(settings.check_for_updates)" > check_updates.txt
set /p CHECK_FOR_UPDATES=<check_updates.txt
del check_updates.txt

if "!CHECK_FOR_UPDATES!"=="True" (
    git fetch origin
    git checkout master
    git pull origin master
)

:: Run the main Python script
"%~dp0venv\Scripts\python.exe" "%~dp0main.py"
pause
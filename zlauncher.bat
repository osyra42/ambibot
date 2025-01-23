@echo off
title Ambibot

REM Change to the directory where the batch file is located
cd /d "%~dp0"

set "music_dir=music"

REM Delete the music directory if it exists
if exist "%music_dir%" (
    echo Deleting all files and subdirectories in %music_dir%...
    del /q /s "%music_dir%\*" >nul
    rmdir /s /q "%music_dir%"
    echo Done.
) else (
    echo Directory %music_dir% does not exist.
)

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
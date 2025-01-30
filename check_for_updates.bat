@echo off
setlocal

:: Read settings.py to check if updates are enabled
"%~dp0venv\Scripts\python.exe" -c "import settings; print(settings.check_for_updates)" > check_updates.txt
set /p CHECK_FOR_UPDATES=<check_updates.txt
del check_updates.txt

:: Only run updates if settings.check_for_updates is True
if "%CHECK_FOR_UPDATES%"=="True" (
    echo Checking for updates...
    set REPO_URL=https://github.com/osyra42/ambibot.git
    set REPO_DIR=ambibot

    if exist "%REPO_DIR%" (
        echo Repository already exists. Fetching updates...
        cd "%REPO_DIR%"
        git fetch origin
        git checkout master
        git pull origin master
    ) else (
        echo Cloning repository...
        git clone "%REPO_URL%" "%REPO_DIR%"
        if errorlevel 1 (
            echo Failed to clone repository.
            exit /b 1
        )
        cd "%REPO_DIR%"
        git checkout master
    )
) else (
    echo Updates are disabled in settings.py.
)

echo Done checking updates.
exit /b
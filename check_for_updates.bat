@echo off
setlocal enabledelayedexpansion

:: Read settings.py to check if updates are enabled
"%~dp0venv\Scripts\python.exe" -c "import settings; print(settings.check_for_updates)" > check_updates.txt
set /p CHECK_FOR_UPDATES=<check_updates.txt
del check_updates.txt

:: Only run updates if settings.check_for_updates is True
if "!CHECK_FOR_UPDATES!"=="True" (
    echo ================================================== >> update_log.txt
    echo Checking for updates... >> update_log.txt
    set REPO_URL=https://github.com/osyra42/ambibot.git
    set REPO_DIR=./

    if exist "!REPO_DIR!" (
        echo Repository already exists. Fetching updates... >> update_log.txt
        cd "!REPO_DIR!"
        git fetch origin >> update_log.txt 2>&1
        if errorlevel 1 (
            echo Failed to fetch updates. >> update_log.txt
            echo Failed to fetch updates.
            exit /b 1
        )
        git checkout master >> update_log.txt 2>&1
        if errorlevel 1 (
            echo Failed to checkout master. >> update_log.txt
            echo Failed to checkout master.
            exit /b 1
        )
        git pull origin master >> update_log.txt 2>&1
        if errorlevel 1 (
            echo Failed to pull updates. >> update_log.txt
            echo Failed to pull updates.
            exit /b 1
        )
    ) else (
        echo Cloning repository... >> update_log.txt
        git clone "!REPO_URL!" "!REPO_DIR!" >> update_log.txt 2>&1
        if errorlevel 1 (
            echo Failed to clone repository. >> update_log.txt
            echo Failed to clone repository.
            exit /b 1
        )
        cd "!REPO_DIR!"
        git checkout master >> update_log.txt 2>&1
        if errorlevel 1 (
            echo Failed to checkout master. >> update_log.txt
            echo Failed to checkout master.
            exit /b 1
        )
    )
) else (
    echo Updates are disabled in settings.py. >> update_log.txt
    echo Updates are disabled in settings.py.
)

echo Done checking updates. >> update_log.txt
echo ================================================== >> update_log.txt
exit /b
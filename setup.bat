@echo off

python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Please install Python before continuing.
    exit /b 1
)

pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo pip is not installed. Please ensure that Python and pip are correctly installed.
    exit /b 1
)

if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo Failed to install dependencies.
        exit /b 1
    )
) else (
    echo requirements.txt not found.
    exit /b 1
)

if exist main.py (
    echo Running main.py...
    python main.py
) else (
    echo main.py not found.
    exit /b 1
)

pause
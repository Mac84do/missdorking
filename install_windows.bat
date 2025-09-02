@echo off
REM Google Dorking Tool - Windows Installation Script
REM MissDorking - Cross-platform Google Dorking Application

echo ============================================
echo    Google Dorking Tool - Windows Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from https://python.org
    echo Make sure to add Python to PATH during installation.
    pause
    exit /b 1
)

echo Python is installed.
python --version

REM Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3,7) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python 3.7 or higher is required.
    echo Please update your Python installation.
    pause
    exit /b 1
)

echo Python version is compatible.
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

REM Create desktop shortcut script
echo Creating launch script...
(
echo @echo off
echo cd /d "%~dp0"
echo call venv\Scripts\activate.bat
echo python main_gui.py
echo pause
) > run_dorking_tool.bat

REM Create start menu shortcut if possible
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs" (
    echo Creating Start Menu shortcut...
    copy run_dorking_tool.bat "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Google Dorking Tool.bat" >nul 2>&1
)

echo.
echo ============================================
echo           Installation Complete!
echo ============================================
echo.
echo The Google Dorking Tool has been successfully installed.
echo.
echo To run the application:
echo   1. Double-click 'run_dorking_tool.bat'
echo   2. Or run: python main_gui.py (from activated venv)
echo.
echo The application has also been added to your Start Menu.
echo.
echo IMPORTANT NOTES:
echo - Use this tool only for authorized security testing
echo - Respect Google's terms of service and rate limits
echo - The tool includes delays to avoid being blocked
echo - Export results to PDF or CSV for analysis
echo.

pause

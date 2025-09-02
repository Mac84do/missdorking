@echo off
REM Enhanced MissDorking Windows Launcher 💋
REM With bulk domains, smart file naming, and fabulous CLI support! 🍒

setlocal enabledelayedexpansion

REM Set colors for fabulous output
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "PINK=%ESC%[95m"
set "RED=%ESC%[91m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "BLUE=%ESC%[94m"
set "CYAN=%ESC%[96m"
set "WHITE=%ESC%[97m"
set "RESET=%ESC%[0m"

REM Change to script directory
cd /d "%~dp0"

echo.
echo %PINK%    💋 MissDorking™ Enhanced Windows Launcher 🍒%RESET%
echo %CYAN%    ╔════════════════════════════════════════════════╗%RESET%
echo %CYAN%    ║  😘  Making Security Fun ^& Fabulous on Windows! 💅 ║%RESET%
echo %CYAN%    ╚════════════════════════════════════════════════╝%RESET%
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo %RED%❌ Virtual environment not found!%RESET%
    echo %YELLOW%💡 Run install_windows.bat first to set up the environment%RESET%
    pause
    exit /b 1
)

REM Activate virtual environment
echo %BLUE%🔧 Activating virtual environment...%RESET%
call venv\Scripts\activate.bat

REM Check if activation was successful
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ Failed to activate Python virtual environment%RESET%
    pause
    exit /b 1
)

echo %GREEN%✅ Virtual environment activated successfully!%RESET%
echo.

:MENU
echo %PINK%💅 Choose your fabulous dorking mode:%RESET%
echo.
echo %CYAN%[1]%RESET% 🎯 GUI Mode - Pretty interface for interactive dorking
echo %CYAN%[2]%RESET% 👑 Enhanced GUI - Super-powered with bulk ^& fun features  
echo %CYAN%[3]%RESET% ⚡ Super Fast GUI - Ludicrously optimized for speed demons
echo %CYAN%[4]%RESET% 💻 CLI Mode - Command line for power users
echo %CYAN%[5]%RESET% 📋 CLI Bulk Mode - Bulk domain processing via CLI
echo %CYAN%[6]%RESET% 🎪 Fun Launcher - Full experience with splash ^& speed test
echo %CYAN%[7]%RESET% 📊 Speed Test - Test the performance improvements
echo %CYAN%[8]%RESET% ❓ Show CLI Help - Display command line options
echo %CYAN%[9]%RESET% 🚪 Exit - Close this fabulous tool
echo.
set /p choice=%YELLOW%💋 Enter your choice (1-9): %RESET%

if "%choice%"=="1" goto GUI_MODE
if "%choice%"=="2" goto ENHANCED_GUI
if "%choice%"=="3" goto SUPER_FAST_GUI
if "%choice%"=="4" goto CLI_MODE
if "%choice%"=="5" goto BULK_CLI_MODE
if "%choice%"=="6" goto FUN_LAUNCHER
if "%choice%"=="7" goto SPEED_TEST
if "%choice%"=="8" goto CLI_HELP
if "%choice%"=="9" goto EXIT
echo %RED%❌ Invalid choice. Please enter 1-9.%RESET%
echo.
goto MENU

:GUI_MODE
echo.
echo %PINK%🎯 Starting original GUI mode...%RESET%
python main_gui.py
goto END

:ENHANCED_GUI
echo.
echo %PINK%👑 Starting enhanced GUI with bulk domains...%RESET%
python main_gui_enhanced.py
goto END

:SUPER_FAST_GUI
echo.
echo %PINK%⚡ Starting super fast optimized GUI...%RESET%
python super_fast_gui.py
goto END

:CLI_MODE
echo.
echo %PINK%💻 CLI Mode - Single Domain Dorking%RESET%
echo.
set /p domain=%CYAN%🎯 Enter domain to scan: %RESET%
if "%domain%"=="" (
    echo %RED%❌ No domain specified%RESET%
    goto MENU
)

echo %CYAN%⚙️ Scan Options:%RESET%
set /p max_results=%CYAN%📊 Max results per query (default 10): %RESET%
if "%max_results%"=="" set max_results=10

set /p delay=%CYAN%⏰ Delay range in seconds (default 2-4): %RESET%
if "%delay%"=="" set delay=2-4

set /p use_hybrid=%CYAN%⚡ Use hybrid scraper for better results? (y/n, default n): %RESET%
if /i "%use_hybrid%"=="y" (
    set hybrid_flag=--hybrid
) else (
    set hybrid_flag=
)

echo.
echo %GREEN%🚀 Starting CLI scan for %domain%...%RESET%
python run_dorking_cli.py -d "%domain%" --max-results %max_results% --delay "%delay%" %hybrid_flag% --export pdf csv
goto END

:BULK_CLI_MODE
echo.
echo %PINK%👑 Bulk CLI Mode - Multiple Domain Domination%RESET%
echo.
echo %CYAN%Choose bulk input method:%RESET%
echo %CYAN%[1]%RESET% 📁 Load from file
echo %CYAN%[2]%RESET% ✍️ Enter domains manually (comma-separated)
echo.
set /p bulk_choice=%YELLOW%💋 Enter choice (1-2): %RESET%

if "%bulk_choice%"=="1" (
    set /p domains_file=%CYAN%📁 Enter path to domains file: %RESET%
    if not exist "!domains_file!" (
        echo %RED%❌ File not found: !domains_file!%RESET%
        goto MENU
    )
    set bulk_input=!domains_file!
) else if "%bulk_choice%"=="2" (
    set /p bulk_input=%CYAN%✍️ Enter domains (comma-separated): %RESET%
    if "!bulk_input!"=="" (
        echo %RED%❌ No domains specified%RESET%
        goto MENU
    )
) else (
    echo %RED%❌ Invalid choice%RESET%
    goto MENU
)

echo %CYAN%📋 Report Format:%RESET%
echo %CYAN%[1]%RESET% Individual reports per domain
echo %CYAN%[2]%RESET% Single combined report for all
echo %CYAN%[3]%RESET% Both individual and combined
echo.
set /p report_choice=%YELLOW%💋 Enter choice (1-3): %RESET%

if "%report_choice%"=="1" set report_format=individual
if "%report_choice%"=="2" set report_format=combined
if "%report_choice%"=="3" set report_format=both
if "%report_format%"=="" set report_format=individual

echo.
echo %GREEN%🚀 Starting bulk CLI scan...%RESET%
python run_dorking_cli.py -b "!bulk_input!" --report-format %report_format% --export pdf csv
goto END

:FUN_LAUNCHER
echo.
echo %PINK%🎪 Starting fun launcher with full experience...%RESET%
python launch_super_fast.py
goto END

:SPEED_TEST
echo.
echo %PINK%📊 Running speed test...%RESET%
python speed_test.py
goto END

:CLI_HELP
echo.
echo %PINK%💻 MissDorking CLI Help %RESET%
echo.
python run_dorking_cli.py --help
echo.
pause
goto MENU

:EXIT
echo.
echo %PINK%💋 Thanks for using MissDorking! Stay fabulous! 🍒%RESET%
goto END

:END
echo.
echo %GREEN%✨ MissDorking operation completed!%RESET%
echo.
set /p restart=%YELLOW%💋 Return to main menu? (y/n): %RESET%
if /i "%restart%"=="y" goto MENU

echo %PINK%💅 Goodbye, fabulous user! 💋%RESET%
pause

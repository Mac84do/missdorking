@echo off
echo ===============================================
echo RECON-OPS v2.0 - Tactical Intelligence Platform
echo ===============================================
echo Starting application...
echo.
cd /d "%~dp0"
python recon_ops.py
if errorlevel 1 (
    echo.
    echo ERROR: Failed to start RECON-OPS
    echo Make sure Python and required modules are installed
    pause
)

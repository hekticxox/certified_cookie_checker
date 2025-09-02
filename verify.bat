@echo off
REM Cookie Verification System - Windows Launcher

echo 🍪 Certified Cookie Checker
echo ===============================

if "%1"=="setup" (
    echo Running production setup...
    python src\setup_production.py
    goto :eof
)

if "%1"=="monitor" (
    echo Starting system monitor...
    python src\system_monitor.py
    goto :eof
)

if "%1"=="help" (
    echo Usage:
    echo   verify.bat [setup^|monitor^|help]
    echo   verify.bat                    - Run verification with personal cookies
    echo   verify.bat setup              - Run production environment setup
    echo   verify.bat monitor            - Monitor running verification process
    echo.
    echo Main verification options ^(use verify_cookies.py for advanced options^):
    echo   python verify_cookies.py --cookies mycookies.txt --headless
    echo   python verify_cookies.py --setup
    echo   python verify_cookies.py --monitor
    goto :eof
)

REM Default: Run verification system
echo Starting cookie verification...
echo ^(Personal files will be saved to personal/ directory^)
echo.

python verify_cookies.py %*

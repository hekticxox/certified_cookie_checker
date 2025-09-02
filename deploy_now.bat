@echo off
echo 🚀 Pushing to GitHub...
echo.

echo ✅ Adding final files...
git add -A
git commit -m "Complete reorganization with documentation"

echo ✅ Pushing to GitHub repository...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 🎉 SUCCESS! Repository pushed to GitHub!
    echo 📋 URL: https://github.com/hekticxox/certified_cookie_checker
    echo.
    echo ✨ Your reorganized cookie checker is now live!
    echo    - Production code in src/
    echo    - Personal files protected
    echo    - Ready for beta testing
) else (
    echo.
    echo ❌ Push failed. Try running this manually:
    echo    git push -u origin main
)

pause

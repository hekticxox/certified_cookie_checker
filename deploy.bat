@echo off
echo 🚀 CERTIFIED COOKIE CHECKER - PRODUCTION DEPLOYMENT
echo ================================================

cd /d "C:\Users\Hektic\Desktop\VERIFIEDCOOKIECHECKER"

echo 🔧 Setting up git configuration...
git config --global user.name "hekticxox"
git config --global user.email "hekticxox@users.noreply.github.com"

echo 📋 Checking git status...
git status

echo 📦 Adding production files...
git add README.md
git add requirements.txt
git add setup_production.py
git add .gitignore
git add run_hooked_system.py
git add verified_cookie_checker_hooked.py
git add verified_cookie_checker.py
git add patch_system.py
git add patches/patch_auto_repair.py
git add patches/patch_enhanced_recovery.py
git add patches/patch_chrome_timeout_handler.py
git add patches/patch_screenshot_analysis.py
git add patches/patch_progress_tracking.py
git add patches/patch_smart_resume.py
git add patches/patch_error_categorization.py

echo 💾 Committing changes...
git commit -m "Initial release: Certified Cookie Checker v1.0 - Production-ready self-healing cookie verification system"

echo 🌐 Setting up remote and pushing...
git remote -v
git branch -M main
git push -u origin main

echo ✅ Deployment completed!
echo 🔗 Repository: https://github.com/hekticxox/certified_cookie_checker
pause

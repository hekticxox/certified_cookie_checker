#!/usr/bin/env python3
"""
Production Deployment Script
Handles git operations and pushes to GitHub
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} timed out")
        return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def main():
    """Main deployment function."""
    print("🚀 CERTIFIED COOKIE CHECKER - PRODUCTION DEPLOYMENT")
    print("=" * 55)
    
    # Change to correct directory
    os.chdir(r"C:\Users\Hektic\Desktop\VERIFIEDCOOKIECHECKER")
    
    # Git configuration
    run_command('git config --global user.name "hekticxox"', "Setting git user name")
    run_command('git config --global user.email "hekticxox@users.noreply.github.com"', "Setting git email")
    
    # Initialize repository if needed
    if not os.path.exists('.git'):
        run_command('git init', "Initializing git repository")
        run_command('git remote add origin https://github.com/hekticxox/certified_cookie_checker.git', "Adding remote origin")
    
    # Check current status
    print("\n📋 Current repository status:")
    run_command('git status --porcelain', "Checking git status")
    
    # Add production files
    production_files = [
        'README.md',
        'requirements.txt', 
        'setup_production.py',
        '.gitignore',
        'run_hooked_system.py',
        'verified_cookie_checker_hooked.py',
        'verified_cookie_checker.py',
        'patch_system.py',
        'patches/patch_auto_repair.py',
        'patches/patch_enhanced_recovery.py', 
        'patches/patch_chrome_timeout_handler.py',
        'patches/patch_screenshot_analysis.py',
        'patches/patch_progress_tracking.py',
        'patches/patch_smart_resume.py',
        'patches/patch_error_categorization.py'
    ]
    
    print("\n📦 Adding production files...")
    for file in production_files:
        if os.path.exists(file):
            run_command(f'git add "{file}"', f"Adding {file}")
            print(f"   ✅ {file}")
        else:
            print(f"   ⚠️ {file} - Not found, skipping")
    
    # Commit changes
    commit_message = '''Initial release: Certified Cookie Checker v1.0

🚀 Production-ready self-healing cookie verification system

Features:
- 🔧 Self-healing: Auto-fixes ChromeDriver, packages, permissions
- 📸 Smart screenshot analysis with visual galleries  
- 🔄 Intelligent resume with exponential backoff
- 📊 Comprehensive reporting and progress tracking
- 🧩 Modular hook-based architecture
- ⚡ Production-ready with robust error handling

Core Components:
- run_hooked_system.py: Main entry point
- verified_cookie_checker_hooked.py: Core verification engine
- patch_system.py: Modular patch loader
- patches/: Self-healing patches for auto-repair
- setup_production.py: Production environment verification

Ready for beta testing with full automation and self-healing capabilities.'''
    
    if run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        print("\n🎯 Ready to push to GitHub!")
        
        # Push to GitHub
        if run_command('git branch -M main', "Setting main branch"):
            if run_command('git push -u origin main', "Pushing to GitHub"):
                print("\n🎉 Successfully deployed to GitHub!")
                print("🔗 Repository: https://github.com/hekticxox/certified_cookie_checker")
                print("\n📋 Next steps for beta testers:")
                print("1. Clone the repository")
                print("2. Run: python setup_production.py")
                print("3. Run: python run_hooked_system.py")
                return True
    
    print("\n❌ Deployment failed. Check errors above.")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

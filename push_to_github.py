#!/usr/bin/env python3
"""
GitHub Deployment Script - Push reorganized repository
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and show the result"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def main():
    print("🚀 Certified Cookie Checker - GitHub Deployment")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not run_command("git status", "Checking git status"):
        print("❌ Not in a git repository or git not available")
        return False
    
    # Add remote if not exists
    run_command("git remote remove origin", "Removing existing origin (if any)")
    if not run_command("git remote add origin https://github.com/hekticxox/certified_cookie_checker.git", "Adding GitHub remote"):
        print("⚠️  Remote might already exist")
    
    # Rename branch to main
    run_command("git branch -M main", "Setting branch to main")
    
    # Show what will be pushed
    run_command("git log --oneline", "Showing commits to push")
    
    # Push to GitHub
    if run_command("git push -u origin main", "Pushing to GitHub"):
        print("\n🎉 Successfully pushed to GitHub!")
        print("📋 Repository: https://github.com/hekticxox/certified_cookie_checker")
        print("\n✨ Your reorganized cookie checker is now live on GitHub!")
        print("   - Production code in src/")
        print("   - Personal files protected by .gitignore") 
        print("   - Ready for beta testing and collaboration")
        return True
    else:
        print("\n❌ Push failed. This might be due to:")
        print("   - Authentication issues")
        print("   - Repository doesn't exist")
        print("   - Network connectivity")
        print("\n💡 Try running manually:")
        print("   git push -u origin main")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Certified Cookie Checker - Production Setup
Run this script to verify your environment is ready for production use.
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def check_required_packages():
    """Check if all required packages are installed."""
    print("\n📦 Checking required packages...")
    
    required_packages = {
        'selenium': '4.15.0',
        'psutil': '5.9.0'
    }
    
    missing_packages = []
    
    for package, min_version in required_packages.items():
        try:
            spec = importlib.util.find_spec(package)
            if spec is None:
                print(f"❌ {package} - Not installed")
                missing_packages.append(package)
            else:
                # Try to get version
                try:
                    module = importlib.import_module(package)
                    version = getattr(module, '__version__', 'Unknown')
                    print(f"✅ {package} {version} - Installed")
                except:
                    print(f"✅ {package} - Installed (version check failed)")
        except ImportError:
            print(f"❌ {package} - Not installed")
            missing_packages.append(package)
    
    return missing_packages

def install_missing_packages(missing_packages):
    """Install missing packages."""
    if not missing_packages:
        return True
    
    print(f"\n🔧 Installing missing packages: {', '.join(missing_packages)}")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def check_chromedriver():
    """Check ChromeDriver status."""
    print("\n🚗 Checking ChromeDriver...")
    
    chromedriver_paths = ['chromedriver.exe', 'chromedriver', './chromedriver', './chromedriver.exe']
    
    for path in chromedriver_paths:
        if os.path.exists(path):
            print(f"✅ ChromeDriver found at: {path}")
            return True
    
    print("⚠️ ChromeDriver not found - will be auto-downloaded on first run")
    return True  # Not critical since we auto-download

def create_directory_structure():
    """Create necessary directory structure."""
    print("\n📁 Setting up directory structure...")
    
    directories = [
        'patches',
        'screenshots_organized/logged_in',
        'screenshots_organized/logged_out', 
        'screenshots_organized/unknown',
        'screenshots_organized/errors'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def verify_core_files():
    """Verify core system files exist."""
    print("\n🔍 Verifying core files...")
    
    core_files = [
        'run_hooked_system.py',
        'verified_cookie_checker_hooked.py',
        'patch_system.py',
        'patches/patch_auto_repair.py',
        'patches/patch_enhanced_recovery.py',
        'patches/patch_chrome_timeout_handler.py'
    ]
    
    missing_files = []
    for file in core_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing!")
            missing_files.append(file)
    
    return len(missing_files) == 0

def run_system_test():
    """Run a quick system test."""
    print("\n🧪 Running system test...")
    
    try:
        # Test patch system loading
        from patch_system import patch_system
        patch_system.load_patches()
        
        patch_count = len(patch_system.loaded_patches)
        print(f"✅ Patch system working - {patch_count} patches loaded")
        
        # List loaded patches
        if patch_count > 0:
            print("   Loaded patches:")
            for patch_name in patch_system.loaded_patches.keys():
                print(f"     - {patch_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    """Main setup verification function."""
    print("🚀 CERTIFIED COOKIE CHECKER - PRODUCTION SETUP")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 6
    
    # Run all checks
    if check_python_version():
        checks_passed += 1
    
    missing_packages = check_required_packages()
    if not missing_packages:
        checks_passed += 1
    else:
        if install_missing_packages(missing_packages):
            checks_passed += 1
    
    if check_chromedriver():
        checks_passed += 1
    
    create_directory_structure()
    checks_passed += 1
    
    if verify_core_files():
        checks_passed += 1
    
    if run_system_test():
        checks_passed += 1
    
    # Final report
    print("\n" + "=" * 50)
    print(f"📊 SETUP VERIFICATION COMPLETE")
    print(f"✅ Passed: {checks_passed}/{total_checks} checks")
    
    if checks_passed == total_checks:
        print("\n🎉 System is ready for production use!")
        print("🚀 Run: python run_hooked_system.py")
        return True
    else:
        print(f"\n⚠️ {total_checks - checks_passed} issues need attention")
        print("🔧 Please fix the issues above before using in production")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

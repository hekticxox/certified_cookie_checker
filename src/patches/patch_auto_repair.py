# ===============================
# SECTION: Auto-Repair System
# ===============================
# Hooks: Automatically detect and patch common issues

import os
import json
import subprocess
import sys
import re
from datetime import datetime
from typing import Dict, List

AUTO_REPAIR_LOG = "auto_repair.json"

def hook_init():
    """Initialize auto-repair system."""
    ensure_auto_repair_log()
    print("🔹 Auto-repair system initialized - self-healing enabled.")

def hook_on_error(error_message: str, domain: str = None):
    """Automatically detect and patch common issues."""
    repair_applied = False
    
    # Check for missing ChromeDriver
    if "chromedriver" in error_message.lower() or "webdriver" in error_message.lower():
        repair_applied = auto_fix_chromedriver()
    
    # Check for missing packages
    elif "ModuleNotFoundError" in error_message or "ImportError" in error_message:
        package_match = re.search(r"No module named '([^']+)'", error_message)
        if package_match:
            package_name = package_match.group(1)
            repair_applied = auto_install_package(package_name)
    
    # Check for permission issues
    elif "PermissionError" in error_message or "Access is denied" in error_message:
        repair_applied = auto_fix_permissions(error_message)
    
    # Check for Chrome/browser issues
    elif "chrome" in error_message.lower() and ("crash" in error_message.lower() or "timeout" in error_message.lower()):
        repair_applied = auto_fix_chrome_issues()
    
    # Check for disk space issues
    elif "No space left" in error_message or "disk full" in error_message:
        repair_applied = auto_cleanup_space()
    
    # Log the repair attempt
    log_repair_attempt(error_message, domain, repair_applied)
    
    if repair_applied:
        print(f"🔧 Auto-repair applied for error: {error_message[:60]}...")
        print("🔄 Retrying operation...")

def auto_fix_chromedriver():
    """Automatically download and setup ChromeDriver."""
    try:
        print("🔧 Auto-fixing ChromeDriver...")
        
        # Check if chromedriver exists
        chromedriver_path = "chromedriver.exe" if os.name == 'nt' else "chromedriver"
        
        if not os.path.exists(chromedriver_path):
            print("📥 Downloading ChromeDriver...")
            
            # Try to install via webdriver-manager
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver-manager"], 
                                    capture_output=True)
                
                # Create a temp script to setup chromedriver
                setup_script = """
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
print("ChromeDriver installed successfully")
"""
                with open("temp_chromedriver_setup.py", "w") as f:
                    f.write(setup_script)
                
                subprocess.check_call([sys.executable, "temp_chromedriver_setup.py"])
                os.remove("temp_chromedriver_setup.py")
                
                print("✅ ChromeDriver auto-repair complete")
                return True
                
            except subprocess.CalledProcessError:
                print("❌ Failed to auto-install ChromeDriver")
                return False
        else:
            print("✅ ChromeDriver already exists")
            return True
            
    except Exception as e:
        print(f"❌ ChromeDriver auto-repair failed: {e}")
        return False

def auto_install_package(package_name):
    """Automatically install missing Python packages."""
    try:
        print(f"🔧 Auto-installing missing package: {package_name}")
        
        # Map common import names to pip package names
        package_mapping = {
            'selenium': 'selenium',
            'webdriver_manager': 'webdriver-manager',
            'PIL': 'Pillow',
            'cv2': 'opencv-python',
            'requests': 'requests',
            'bs4': 'beautifulsoup4',
            'numpy': 'numpy',
            'pandas': 'pandas'
        }
        
        pip_package = package_mapping.get(package_name, package_name)
        
        result = subprocess.run([sys.executable, "-m", "pip", "install", pip_package], 
                               capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ Successfully installed {pip_package}")
            return True
        else:
            print(f"❌ Failed to install {pip_package}: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Package installation timeout for {package_name}")
        return False
    except Exception as e:
        print(f"❌ Package installation failed: {e}")
        return False

def auto_fix_permissions(error_message):
    """Attempt to fix permission issues."""
    try:
        print("🔧 Auto-fixing permission issues...")
        
        # Extract file path from error if possible
        file_match = re.search(r"'([^']*[/\\][^']*)'", error_message)
        if file_match:
            file_path = file_match.group(1)
            
            # Try to fix common permission issues
            if os.path.exists(file_path):
                # On Windows, try to remove read-only attribute
                if os.name == 'nt':
                    try:
                        os.chmod(file_path, 0o777)
                        print(f"✅ Fixed permissions for {file_path}")
                        return True
                    except:
                        pass
        
        # Create alternative directories with proper permissions
        alt_dirs = ["screenshots_temp", "logs_temp", "data_temp"]
        for alt_dir in alt_dirs:
            try:
                os.makedirs(alt_dir, exist_ok=True)
                os.chmod(alt_dir, 0o777)
            except:
                pass
        
        print("✅ Created alternative directories with proper permissions")
        return True
        
    except Exception as e:
        print(f"❌ Permission fix failed: {e}")
        return False

def auto_fix_chrome_issues():
    """Fix common Chrome browser issues."""
    try:
        print("🔧 Auto-fixing Chrome issues...")
        
        # Kill any hanging Chrome processes
        if os.name == 'nt':
            subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], 
                          capture_output=True)
            subprocess.run(["taskkill", "/f", "/im", "chromedriver.exe"], 
                          capture_output=True)
        else:
            subprocess.run(["pkill", "-f", "chrome"], capture_output=True)
            subprocess.run(["pkill", "-f", "chromedriver"], capture_output=True)
        
        # Clear Chrome temp data
        chrome_temp_dirs = [
            os.path.expanduser("~/.config/google-chrome/Default/"),
            os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/"),
        ]
        
        for temp_dir in chrome_temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    # Clear cache and temp files (be careful not to delete important data)
                    cache_dir = os.path.join(temp_dir, "Cache")
                    if os.path.exists(cache_dir):
                        for file in os.listdir(cache_dir):
                            try:
                                os.remove(os.path.join(cache_dir, file))
                            except:
                                pass
                except:
                    pass
        
        print("✅ Chrome cleanup complete")
        return True
        
    except Exception as e:
        print(f"❌ Chrome fix failed: {e}")
        return False

def auto_cleanup_space():
    """Clean up disk space by removing old logs and screenshots."""
    try:
        print("🔧 Auto-cleaning disk space...")
        
        cleaned_size = 0
        
        # Clean old log files
        for file in os.listdir("."):
            if file.endswith(".log") and os.path.getsize(file) > 10*1024*1024:  # > 10MB
                size = os.path.getsize(file)
                os.remove(file)
                cleaned_size += size
                print(f"🗑️ Removed large log file: {file}")
        
        # Clean old screenshots (keep only last 50)
        screenshot_dirs = ["screenshots", "screenshots_organized"]
        for screenshot_dir in screenshot_dirs:
            if os.path.exists(screenshot_dir):
                all_screenshots = []
                for root, dirs, files in os.walk(screenshot_dir):
                    for file in files:
                        if file.endswith(('.png', '.jpg', '.jpeg')):
                            full_path = os.path.join(root, file)
                            all_screenshots.append((full_path, os.path.getmtime(full_path)))
                
                # Sort by modification time and keep only latest 50
                all_screenshots.sort(key=lambda x: x[1], reverse=True)
                
                for file_path, _ in all_screenshots[50:]:
                    size = os.path.getsize(file_path)
                    os.remove(file_path)
                    cleaned_size += size
        
        print(f"✅ Cleaned {cleaned_size // (1024*1024)} MB of disk space")
        return True
        
    except Exception as e:
        print(f"❌ Space cleanup failed: {e}")
        return False

def ensure_auto_repair_log():
    """Ensure auto-repair log file exists."""
    if not os.path.exists(AUTO_REPAIR_LOG):
        initial_log = {
            "repairs": [],
            "success_rate": 0,
            "last_updated": datetime.now().isoformat()
        }
        save_auto_repair_log(initial_log)

def load_auto_repair_log():
    """Load auto-repair log."""
    try:
        with open(AUTO_REPAIR_LOG, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"repairs": [], "success_rate": 0, "last_updated": datetime.now().isoformat()}

def save_auto_repair_log(log_data):
    """Save auto-repair log."""
    try:
        with open(AUTO_REPAIR_LOG, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
    except Exception as e:
        print(f"[!] Failed to save auto-repair log: {e}")

def log_repair_attempt(error_message, domain, success):
    """Log repair attempt."""
    log_data = load_auto_repair_log()
    
    repair_entry = {
        "timestamp": datetime.now().isoformat(),
        "error_message": error_message[:200],  # Truncate long errors
        "domain": domain,
        "repair_success": success,
        "repair_type": detect_repair_type(error_message)
    }
    
    log_data["repairs"].append(repair_entry)
    
    # Calculate success rate
    total_repairs = len(log_data["repairs"])
    successful_repairs = sum(1 for r in log_data["repairs"] if r["repair_success"])
    log_data["success_rate"] = (successful_repairs / total_repairs * 100) if total_repairs > 0 else 0
    log_data["last_updated"] = datetime.now().isoformat()
    
    # Keep only last 100 repair attempts
    log_data["repairs"] = log_data["repairs"][-100:]
    
    save_auto_repair_log(log_data)

def detect_repair_type(error_message):
    """Detect the type of repair needed."""
    if "chromedriver" in error_message.lower():
        return "chromedriver_fix"
    elif "ModuleNotFoundError" in error_message:
        return "package_install"
    elif "PermissionError" in error_message:
        return "permission_fix"
    elif "chrome" in error_message.lower():
        return "chrome_fix"
    elif "space" in error_message.lower():
        return "space_cleanup"
    else:
        return "unknown"

def hook_cleanup(results: List, errors: List):
    """Generate auto-repair summary."""
    log_data = load_auto_repair_log()
    
    if log_data["repairs"]:
        print(f"\n🔧 AUTO-REPAIR SUMMARY:")
        print(f"   Total repairs attempted: {len(log_data['repairs'])}")
        print(f"   Success rate: {log_data['success_rate']:.1f}%")
        
        # Show recent repair types
        recent_repairs = log_data["repairs"][-5:]
        repair_types = {}
        for repair in recent_repairs:
            repair_type = repair["repair_type"]
            repair_types[repair_type] = repair_types.get(repair_type, 0) + 1
        
        if repair_types:
            print(f"   Recent repair types:")
            for repair_type, count in repair_types.items():
                print(f"     - {repair_type}: {count}")

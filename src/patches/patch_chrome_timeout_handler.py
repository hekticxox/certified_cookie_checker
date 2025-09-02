# ===============================
# SECTION: Chrome Startup & Timeout Handler
# ===============================
# Hooks: Handle Chrome startup issues and timeout problems

import os
import time
import signal
import subprocess
import psutil
from datetime import datetime
from typing import Dict, List

CHROME_STARTUP_TIMEOUT = 30  # seconds
CHROME_OPERATION_TIMEOUT = 60  # seconds

def hook_init():
    """Initialize Chrome startup handler."""
    cleanup_hanging_chrome_processes()
    print("🔹 Chrome startup & timeout handler initialized.")

def hook_before_run(domain: str = None, cookies: List = None):
    """Pre-startup Chrome health checks."""
    if not domain:
        return
    
    print(f"🔍 Pre-flight checks for {domain}...")
    
    # Check if Chrome processes are already running and potentially hung
    hung_processes = find_hung_chrome_processes()
    if hung_processes:
        print(f"🧹 Found {len(hung_processes)} potentially hung Chrome processes")
        cleanup_hanging_chrome_processes()
    
    # Check available memory
    memory_available = get_available_memory_mb()
    if memory_available < 500:  # Less than 500MB available
        print(f"⚠️ Low memory detected: {memory_available}MB available")
        free_up_memory()
    
    # Pre-create directories to avoid permission issues
    ensure_chrome_directories()

def hook_on_error(error_message: str, domain: str = None):
    """Handle Chrome-specific timeout and startup errors."""
    if not domain:
        return
    
    error_lower = error_message.lower()
    
    # Chrome startup timeout
    if "timeout" in error_lower or "timed out" in error_lower:
        print(f"🔧 Handling timeout for {domain}...")
        apply_timeout_fix(domain)
        
    # Chrome crash or hang
    elif "chrome" in error_lower and ("crash" in error_lower or "hang" in error_lower):
        print(f"🔧 Handling Chrome crash for {domain}...")
        apply_chrome_crash_fix(domain)
        
    # WebDriver connection issues
    elif "webdriver" in error_lower and "connect" in error_lower:
        print(f"🔧 Handling WebDriver connection issue for {domain}...")
        apply_webdriver_connection_fix(domain)

def find_hung_chrome_processes():
    """Find Chrome processes that might be hung."""
    hung_processes = []
    current_time = time.time()
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            if proc.info['name'] and ('chrome' in proc.info['name'].lower() or 'chromedriver' in proc.info['name'].lower()):
                # Process running for more than 5 minutes might be hung
                if current_time - proc.info['create_time'] > 300:
                    hung_processes.append(proc)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    
    return hung_processes

def cleanup_hanging_chrome_processes():
    """Force kill hanging Chrome and ChromeDriver processes."""
    try:
        if os.name == 'nt':  # Windows
            # Kill Chrome processes
            subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], 
                          capture_output=True, timeout=10)
            subprocess.run(['taskkill', '/f', '/im', 'chromedriver.exe'], 
                          capture_output=True, timeout=10)
            
            # Also kill any hung browser processes
            subprocess.run(['taskkill', '/f', '/im', 'msedge.exe'], 
                          capture_output=True, timeout=10)
        else:  # Linux/Mac
            subprocess.run(['pkill', '-f', 'chrome'], capture_output=True, timeout=10)
            subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True, timeout=10)
        
        print("🧹 Cleaned up hanging browser processes")
        time.sleep(2)  # Give processes time to terminate
        
    except subprocess.TimeoutExpired:
        print("⚠️ Process cleanup timeout - some processes may still be running")
    except Exception as e:
        print(f"⚠️ Process cleanup error: {e}")

def get_available_memory_mb():
    """Get available system memory in MB."""
    try:
        memory = psutil.virtual_memory()
        return memory.available // (1024 * 1024)
    except:
        return 1000  # Default assumption

def free_up_memory():
    """Attempt to free up system memory."""
    try:
        # Force garbage collection
        import gc
        gc.collect()
        
        # Clear any cached files in temp directories
        temp_dirs = [
            os.path.expanduser("~/AppData/Local/Temp"),
            "/tmp",
            "screenshots_temp",
            "logs_temp"
        ]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    # Remove files older than 1 hour
                    current_time = time.time()
                    for file in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, file)
                        if os.path.isfile(file_path):
                            if current_time - os.path.getmtime(file_path) > 3600:
                                os.remove(file_path)
                except:
                    pass
        
        print("🧹 Memory cleanup completed")
        
    except Exception as e:
        print(f"⚠️ Memory cleanup error: {e}")

def ensure_chrome_directories():
    """Ensure Chrome can write to necessary directories."""
    try:
        # Create temp directories with proper permissions
        temp_dirs = ["chrome_temp", "screenshots_temp", "downloads_temp"]
        
        for dir_name in temp_dirs:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
                if os.name != 'nt':  # Unix-like systems
                    os.chmod(dir_name, 0o755)
        
    except Exception as e:
        print(f"⚠️ Directory setup error: {e}")

def apply_timeout_fix(domain):
    """Apply specific fixes for timeout issues."""
    print(f"🔧 Applying timeout fix for {domain}...")
    
    # Strategy 1: Kill all Chrome processes and wait
    cleanup_hanging_chrome_processes()
    time.sleep(5)
    
    # Strategy 2: Clear Chrome cache and user data
    clear_chrome_user_data()
    
    # Strategy 3: Create timeout recovery file
    create_timeout_recovery_marker(domain)

def apply_chrome_crash_fix(domain):
    """Apply specific fixes for Chrome crashes."""
    print(f"🔧 Applying Chrome crash fix for {domain}...")
    
    # Kill processes
    cleanup_hanging_chrome_processes()
    
    # Clear crash reports
    clear_chrome_crash_data()
    
    # Reset Chrome flags
    create_chrome_recovery_flags()

def apply_webdriver_connection_fix(domain):
    """Apply specific fixes for WebDriver connection issues."""
    print(f"🔧 Applying WebDriver connection fix for {domain}...")
    
    # Kill ChromeDriver specifically
    if os.name == 'nt':
        subprocess.run(['taskkill', '/f', '/im', 'chromedriver.exe'], capture_output=True)
    else:
        subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True)
    
    time.sleep(3)
    
    # Check ChromeDriver file
    if os.path.exists('chromedriver.exe'):
        # Test if ChromeDriver is working
        try:
            result = subprocess.run(['chromedriver.exe', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print("🔧 ChromeDriver appears corrupted, will re-download...")
                os.remove('chromedriver.exe')
        except:
            print("🔧 ChromeDriver test failed, will re-download...")
            try:
                os.remove('chromedriver.exe')
            except:
                pass

def clear_chrome_user_data():
    """Clear Chrome user data that might be causing issues."""
    try:
        user_data_paths = [
            os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/"),
            os.path.expanduser("~/.config/google-chrome/Default/"),
            "chrome_temp"
        ]
        
        for user_data_path in user_data_paths:
            if os.path.exists(user_data_path):
                # Clear specific problematic files
                problem_files = ["Preferences", "Local State", "Cookies", "Cache"]
                
                for problem_file in problem_files:
                    file_path = os.path.join(user_data_path, problem_file)
                    if os.path.exists(file_path):
                        try:
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                            elif os.path.isdir(file_path):
                                import shutil
                                shutil.rmtree(file_path, ignore_errors=True)
                        except:
                            pass
        
        print("🧹 Chrome user data cleared")
        
    except Exception as e:
        print(f"⚠️ Chrome user data cleanup error: {e}")

def clear_chrome_crash_data():
    """Clear Chrome crash reports and dumps."""
    try:
        crash_paths = [
            os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Crashpad/"),
            os.path.expanduser("~/.config/google-chrome/Crash Reports/"),
        ]
        
        for crash_path in crash_paths:
            if os.path.exists(crash_path):
                import shutil
                shutil.rmtree(crash_path, ignore_errors=True)
        
        print("🧹 Chrome crash data cleared")
        
    except Exception as e:
        print(f"⚠️ Chrome crash cleanup error: {e}")

def create_chrome_recovery_flags():
    """Create Chrome flags file for better stability."""
    try:
        flags_content = """--no-sandbox
--disable-dev-shm-usage
--disable-gpu
--disable-software-rasterizer
--disable-background-timer-throttling
--disable-backgrounding-occluded-windows
--disable-renderer-backgrounding
--disable-features=TranslateUI
--disable-extensions
--disable-plugins
--disable-default-apps
--no-first-run
--no-default-browser-check
--disable-background-networking
"""
        
        with open("chrome_recovery_flags.txt", "w") as f:
            f.write(flags_content)
        
        print("🔧 Chrome recovery flags created")
        
    except Exception as e:
        print(f"⚠️ Chrome flags creation error: {e}")

def create_timeout_recovery_marker(domain):
    """Create a marker file for domains that timeout frequently."""
    try:
        recovery_data = {
            "domain": domain,
            "timeout_timestamp": datetime.now().isoformat(),
            "recovery_strategy": "increased_timeouts",
            "suggested_flags": ["--disable-web-security", "--disable-features=VizDisplayCompositor"]
        }
        
        with open(f"timeout_recovery_{domain.replace('.', '_').replace(':', '_')}.json", "w") as f:
            import json
            json.dump(recovery_data, f, indent=2)
        
        print(f"📝 Timeout recovery marker created for {domain}")
        
    except Exception as e:
        print(f"⚠️ Recovery marker creation error: {e}")

def hook_cleanup(results: List, errors: List):
    """Final cleanup of Chrome processes and temp files."""
    print("\n🧹 Final Chrome cleanup...")
    
    # One final cleanup of any remaining processes
    cleanup_hanging_chrome_processes()
    
    # Clean up temporary files
    temp_files = ["chrome_recovery_flags.txt"]
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
    
    print("✅ Chrome cleanup completed")

# ===============================
# SECTION: Aggressive Timeout & Domain Blacklist
# ===============================
# Hooks: Handle problematic domains with aggressive timeouts

import os
import threading
import time
import signal
import subprocess
from datetime import datetime
from typing import Dict, List

# Known problematic domains that often hang
PROBLEMATIC_DOMAINS = {
    'www.futbin.com': {'reason': 'Heavy JavaScript, often hangs', 'timeout': 15},
    'futbin.com': {'reason': 'Heavy JavaScript, often hangs', 'timeout': 15},
    'instagram.com': {'reason': 'Anti-automation detection', 'timeout': 10},
    'facebook.com': {'reason': 'Complex auth flow', 'timeout': 10},
    'twitter.com': {'reason': 'Rate limiting', 'timeout': 10},
    'x.com': {'reason': 'Rate limiting', 'timeout': 10}
}

# Global timeout thread
timeout_thread = None
operation_cancelled = False

def hook_init():
    """Initialize aggressive timeout handler."""
    print("🔹 Aggressive timeout & domain blacklist initialized.")
    
    # Create emergency kill script
    create_emergency_kill_script()

def hook_before_run(domain: str = None, cookies: List = None):
    """Apply domain-specific handling and start timeout watchdog."""
    global timeout_thread, operation_cancelled
    
    if not domain:
        return
    
    operation_cancelled = False
    
    # Check if domain is known to be problematic
    if domain in PROBLEMATIC_DOMAINS:
        info = PROBLEMATIC_DOMAINS[domain]
        print(f"⚠️ WARNING: {domain} is known to be problematic!")
        print(f"   Reason: {info['reason']}")
        print(f"   Using reduced timeout: {info['timeout']} seconds")
        
        # Start aggressive timeout thread
        timeout_duration = info['timeout']
    else:
        timeout_duration = 30  # Default timeout
    
    # Start watchdog thread
    timeout_thread = threading.Thread(
        target=timeout_watchdog, 
        args=(domain, timeout_duration),
        daemon=True
    )
    timeout_thread.start()
    
    print(f"🕐 Timeout watchdog started: {timeout_duration}s limit for {domain}")

def hook_after_run(result: Dict):
    """Stop timeout watchdog after successful run."""
    global operation_cancelled
    operation_cancelled = True
    print("✅ Operation completed - timeout watchdog stopped")

def hook_on_error(error_message: str, domain: str = None):
    """Handle timeout errors and add to blacklist if needed."""
    global operation_cancelled
    operation_cancelled = True
    
    if domain and "timeout" in error_message.lower():
        print(f"⚠️ Timeout detected for {domain}")
        
        # Add to problematic domains list if not already there
        if domain not in PROBLEMATIC_DOMAINS:
            PROBLEMATIC_DOMAINS[domain] = {
                'reason': 'Frequent timeouts detected',
                'timeout': 10
            }
            save_problematic_domains()
            print(f"📝 Added {domain} to problematic domains list")
        
        # Force kill any remaining Chrome processes
        force_kill_chrome()

def timeout_watchdog(domain: str, timeout_seconds: int):
    """Aggressive timeout watchdog that kills Chrome if it hangs."""
    global operation_cancelled
    
    start_time = time.time()
    
    while not operation_cancelled and (time.time() - start_time) < timeout_seconds:
        time.sleep(1)
    
    if not operation_cancelled:
        print(f"\n🚨 TIMEOUT WATCHDOG TRIGGERED for {domain}!")
        print(f"   Operation exceeded {timeout_seconds} seconds")
        print("   Force-killing Chrome processes...")
        
        # Force kill Chrome
        force_kill_chrome()
        
        # Mark as problematic
        if domain not in PROBLEMATIC_DOMAINS:
            PROBLEMATIC_DOMAINS[domain] = {
                'reason': f'Timeout after {timeout_seconds}s',
                'timeout': max(10, timeout_seconds // 2)
            }
            save_problematic_domains()
        
        print(f"💀 Killed hanging processes for {domain}")

def force_kill_chrome():
    """Aggressively kill all Chrome processes."""
    try:
        if os.name == 'nt':  # Windows
            # Kill with extreme prejudice
            subprocess.run(['taskkill', '/f', '/t', '/im', 'chrome.exe'], 
                          capture_output=True, timeout=5)
            subprocess.run(['taskkill', '/f', '/t', '/im', 'chromedriver.exe'], 
                          capture_output=True, timeout=5)
            
            # Also kill any Edge processes that might be interfering
            subprocess.run(['taskkill', '/f', '/t', '/im', 'msedge.exe'], 
                          capture_output=True, timeout=5)
            subprocess.run(['taskkill', '/f', '/t', '/im', 'msedgewebview2.exe'], 
                          capture_output=True, timeout=5)
        
        time.sleep(2)  # Give processes time to die
        
        # Use Python to kill any remaining processes
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and any(name in proc.info['name'].lower() 
                                           for name in ['chrome', 'chromedriver', 'msedge']):
                    try:
                        proc.kill()
                    except:
                        pass
        except ImportError:
            pass
        
        print("💀 Force-killed all browser processes")
        
    except Exception as e:
        print(f"⚠️ Force kill error: {e}")

def create_emergency_kill_script():
    """Create a standalone emergency kill script."""
    script_content = '''@echo off
echo 🚨 EMERGENCY CHROME KILLER
echo Killing all Chrome processes...
taskkill /f /t /im chrome.exe 2>nul
taskkill /f /t /im chromedriver.exe 2>nul
taskkill /f /t /im msedge.exe 2>nul
taskkill /f /t /im msedgewebview2.exe 2>nul
echo ✅ Process kill completed
pause
'''
    
    try:
        with open("EMERGENCY_KILL_CHROME.bat", "w") as f:
            f.write(script_content)
        print("🚨 Emergency kill script created: EMERGENCY_KILL_CHROME.bat")
    except:
        pass

def save_problematic_domains():
    """Save problematic domains to file."""
    try:
        import json
        with open("problematic_domains.json", "w") as f:
            json.dump(PROBLEMATIC_DOMAINS, f, indent=2)
    except Exception as e:
        print(f"⚠️ Failed to save problematic domains: {e}")

def load_problematic_domains():
    """Load problematic domains from file."""
    global PROBLEMATIC_DOMAINS
    try:
        import json
        if os.path.exists("problematic_domains.json"):
            with open("problematic_domains.json", "r") as f:
                loaded = json.load(f)
                PROBLEMATIC_DOMAINS.update(loaded)
    except Exception as e:
        print(f"⚠️ Failed to load problematic domains: {e}")

def hook_cleanup(results: List, errors: List):
    """Final cleanup and report problematic domains."""
    global operation_cancelled
    operation_cancelled = True
    
    # Save updated problematic domains
    save_problematic_domains()
    
    # Report problematic domains
    if PROBLEMATIC_DOMAINS:
        print(f"\n⚠️ PROBLEMATIC DOMAINS DETECTED:")
        for domain, info in PROBLEMATIC_DOMAINS.items():
            print(f"   - {domain}: {info['reason']} (timeout: {info['timeout']}s)")
    
    # Final force kill to be sure
    force_kill_chrome()

# Load existing problematic domains on import
load_problematic_domains()

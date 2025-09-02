#!/usr/bin/env python3
"""
Real-time Cookie Verification Monitor
Shows what the system is currently doing and why it might be taking long
"""

import os
import json
import time
import psutil
from datetime import datetime

def check_running_processes():
    """Check if cookie verification is still running."""
    print("🔍 CHECKING RUNNING PROCESSES")
    print("=" * 40)
    
    python_processes = []
    chrome_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if 'run_hooked_system' in cmdline or 'verified_cookie_checker' in cmdline:
                    runtime = time.time() - proc.info['create_time']
                    python_processes.append({
                        'pid': proc.info['pid'],
                        'cmdline': cmdline[:80] + '...' if len(cmdline) > 80 else cmdline,
                        'runtime': f"{int(runtime//60)}m {int(runtime%60)}s"
                    })
            
            elif proc.info['name'] and ('chrome' in proc.info['name'].lower() or 'chromedriver' in proc.info['name'].lower()):
                runtime = time.time() - proc.info['create_time']
                chrome_processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'runtime': f"{int(runtime//60)}m {int(runtime%60)}s"
                })
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if python_processes:
        print(f"🐍 PYTHON PROCESSES ({len(python_processes)}):")
        for proc in python_processes:
            print(f"   PID {proc['pid']}: {proc['cmdline']} (Running: {proc['runtime']})")
    else:
        print("❌ No Python cookie verification processes found")
    
    if chrome_processes:
        print(f"\n🌐 CHROME PROCESSES ({len(chrome_processes)}):")
        for proc in chrome_processes[:5]:  # Show first 5
            print(f"   PID {proc['pid']}: {proc['name']} (Running: {proc['runtime']})")
        if len(chrome_processes) > 5:
            print(f"   ... and {len(chrome_processes) - 5} more chrome processes")
    else:
        print("❌ No Chrome processes found")
    
    return len(python_processes) > 0, len(chrome_processes)

def analyze_progress_files():
    """Analyze progress from generated files."""
    print(f"\n📊 PROGRESS ANALYSIS")
    print("=" * 40)
    
    # Check resume state
    if os.path.exists("resume_state.json"):
        with open("resume_state.json", 'r') as f:
            resume_data = json.load(f)
        
        successful = len(resume_data.get("successful_domains", {}))
        failures = len(resume_data.get("recent_failures", {}))
        
        print(f"✅ Successful domains: {successful}")
        print(f"❌ Recent failures: {failures}")
        
        if successful > 0:
            print("📋 Recent successful domains:")
            for domain, info in list(resume_data.get("successful_domains", {}).items())[-3:]:
                timestamp = info.get("timestamp", "")[:19].replace("T", " ")
                cookies = info.get("cookies_injected", 0)
                print(f"   - {domain}: {cookies} cookies @ {timestamp}")
        
        if failures > 0:
            print("⚠️ Recent failed domains:")
            for domain, timestamp in list(resume_data.get("recent_failures", {}).items())[-3:]:
                timestamp = timestamp[:19].replace("T", " ")
                print(f"   - {domain} @ {timestamp}")
    
    # Check auto-repair log
    if os.path.exists("auto_repair.json"):
        with open("auto_repair.json", 'r') as f:
            repair_data = json.load(f)
        
        repairs = len(repair_data.get("repairs", []))
        success_rate = repair_data.get("success_rate", 0)
        
        print(f"\n🔧 Auto-repairs attempted: {repairs}")
        print(f"🎯 Repair success rate: {success_rate:.1f}%")
    
    # Check screenshots
    screenshot_count = 0
    if os.path.exists("screenshots_organized"):
        for folder in ["logged_in", "logged_out", "unknown", "errors"]:
            folder_path = os.path.join("screenshots_organized", folder)
            if os.path.exists(folder_path):
                count = len([f for f in os.listdir(folder_path) if f.endswith('.png')])
                screenshot_count += count
                if count > 0:
                    print(f"📸 {folder.replace('_', ' ').title()}: {count} screenshots")
    
    print(f"📸 Total screenshots: {screenshot_count}")

def check_potential_issues():
    """Check for potential issues causing slowness."""
    print(f"\n⚠️ POTENTIAL ISSUES")
    print("=" * 40)
    
    issues_found = []
    
    # Check memory usage
    memory = psutil.virtual_memory()
    if memory.percent > 85:
        issues_found.append(f"High memory usage: {memory.percent:.1f}%")
    
    # Check disk space
    disk = psutil.disk_usage('.')
    if disk.percent > 90:
        issues_found.append(f"Low disk space: {disk.percent:.1f}% used")
    
    # Check for too many chrome processes
    chrome_count = len([p for p in psutil.process_iter(['name']) 
                       if p.info['name'] and 'chrome' in p.info['name'].lower()])
    if chrome_count > 20:
        issues_found.append(f"Too many Chrome processes: {chrome_count}")
    
    # Check for hanging timeout files
    timeout_files = [f for f in os.listdir('.') if f.startswith('timeout_recovery_')]
    if len(timeout_files) > 5:
        issues_found.append(f"Many timeout recovery files: {len(timeout_files)}")
    
    # Check if domain filters are too restrictive
    if os.path.exists("domain_filters.json"):
        with open("domain_filters.json", 'r') as f:
            filters = json.load(f)
        skip_count = len(filters.get("skip_domains", []))
        if skip_count > 10:
            issues_found.append(f"Many domains being skipped: {skip_count}")
    
    if issues_found:
        for issue in issues_found:
            print(f"⚠️ {issue}")
    else:
        print("✅ No obvious issues detected")

def estimate_remaining_time():
    """Estimate how much longer the process might take."""
    print(f"\n⏱️ TIME ESTIMATION")
    print("=" * 40)
    
    if os.path.exists("resume_state.json"):
        with open("resume_state.json", 'r') as f:
            resume_data = json.load(f)
        
        successful = len(resume_data.get("successful_domains", {}))
        
        if successful > 0:
            # Estimate based on successful domains processed
            # You mentioned 16 cookie files, let's assume ~10 domains per file = 160 total
            estimated_total = 160
            remaining = max(0, estimated_total - successful)
            
            # Estimate ~30 seconds per domain (including auto-repair time)
            estimated_seconds = remaining * 30
            estimated_minutes = estimated_seconds // 60
            
            print(f"📊 Estimated progress: {successful}/{estimated_total} domains")
            print(f"⏳ Estimated remaining time: {estimated_minutes} minutes")
            print(f"🎯 Completion estimate: {(successful/estimated_total)*100:.1f}%")
        else:
            print("❓ Unable to estimate - no successful domains yet")

def main():
    print(f"🔍 COOKIE VERIFICATION SYSTEM MONITOR")
    print(f"⏰ Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    is_running, chrome_count = check_running_processes()
    analyze_progress_files()
    check_potential_issues()
    estimate_remaining_time()
    
    print("\n" + "=" * 50)
    
    if is_running:
        print("🟢 SYSTEM STATUS: RUNNING")
        print("💡 The system appears to be actively processing domains")
        if chrome_count > 10:
            print("⚠️ Many Chrome processes detected - this is normal but may slow things down")
    else:
        print("🔴 SYSTEM STATUS: NOT RUNNING")
        print("💡 The cookie verification process may have completed or stopped")
    
    print("\n🛠️ ACTIONS YOU CAN TAKE:")
    print("- Wait longer (large cookie sets take time)")
    print("- Run 'python emergency_chrome_fix.py' if too many Chrome processes")
    print("- Check the screenshots_organized/ folder for current results")
    print("- Press Ctrl+C to stop if needed and check partial results")

if __name__ == "__main__":
    main()

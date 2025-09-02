# ===============================
# SECTION: Screenshot Analysis & Visual Logging
# ===============================
# Hooks: Analyze screenshots and provide visual feedback

import os
import shutil
from datetime import datetime
from typing import Dict, List

SCREENSHOTS_DIR = "screenshots_organized"

def hook_init():
    """Initialize screenshot organization system."""
    if not os.path.exists(SCREENSHOTS_DIR):
        os.makedirs(SCREENSHOTS_DIR)
    
    # Create subdirectories
    for subdir in ['logged_in', 'logged_out', 'errors', 'unknown']:
        subdir_path = os.path.join(SCREENSHOTS_DIR, subdir)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)
    
    print("🔹 Screenshot organization system initialized.")

def hook_on_success(result: Dict):
    """Organize screenshots based on results."""
    screenshot_path = result.get('screenshot')
    if not screenshot_path or not os.path.exists(screenshot_path):
        return
    
    domain = result.get('domain', 'unknown').lstrip('.')
    logged_in_status = result.get('logged_in')
    
    # Determine target directory
    if logged_in_status is True:
        target_dir = os.path.join(SCREENSHOTS_DIR, 'logged_in')
        status = "LOGGED_IN"
    elif logged_in_status is False:
        target_dir = os.path.join(SCREENSHOTS_DIR, 'logged_out')
        status = "LOGGED_OUT"
    else:
        target_dir = os.path.join(SCREENSHOTS_DIR, 'unknown')
        status = "UNKNOWN"
    
    # Create organized filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{status}_{domain}_{timestamp}.png"
    target_path = os.path.join(target_dir, new_filename)
    
    try:
        shutil.copy2(screenshot_path, target_path)
        print(f"[i] Screenshot organized: {new_filename}")
        
        # Update result with organized path
        result['organized_screenshot'] = target_path
        
    except Exception as e:
        print(f"[!] Failed to organize screenshot for {domain}: {e}")

def hook_on_error(error_message: str, domain: str = None):
    """Handle screenshots for failed domains."""
    if domain:
        # Check if there's a screenshot for this domain that needs to be moved to errors
        domain_clean = domain.lstrip('.')
        possible_screenshot = f"{domain_clean}_screenshot.png"
        
        # Look for screenshot in common locations
        for base_path in ['.', 'screenshots']:
            screenshot_path = os.path.join(base_path, possible_screenshot)
            if os.path.exists(screenshot_path):
                target_dir = os.path.join(SCREENSHOTS_DIR, 'errors')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"ERROR_{domain_clean}_{timestamp}.png"
                target_path = os.path.join(target_dir, new_filename)
                
                try:
                    shutil.copy2(screenshot_path, target_path)
                    print(f"[i] Error screenshot organized: {new_filename}")
                except Exception as e:
                    print(f"[!] Failed to organize error screenshot: {e}")
                break

def hook_cleanup(results: List, errors: List):
    """Generate screenshot summary report."""
    report_path = os.path.join(SCREENSHOTS_DIR, 'screenshot_report.txt')
    
    logged_in_count = len([r for r in results if r.get('logged_in') is True])
    logged_out_count = len([r for r in results if r.get('logged_in') is False])
    unknown_count = len([r for r in results if r.get('logged_in') is None and not r.get('error')])
    error_count = len([r for r in results if r.get('error')])
    
    report_content = f"""Screenshot Organization Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Summary:
- Logged In Sessions: {logged_in_count}
- Logged Out Sessions: {logged_out_count}
- Unknown Status: {unknown_count}
- Errors: {error_count}
- Total Screenshots: {logged_in_count + logged_out_count + unknown_count + error_count}

Organization:
- screenshots_organized/logged_in/: Screenshots showing successful logins
- screenshots_organized/logged_out/: Screenshots showing logged out state
- screenshots_organized/unknown/: Screenshots from headless mode (status unknown)
- screenshots_organized/errors/: Screenshots from failed attempts

Detailed Results:
"""
    
    for result in results:
        domain = result.get('domain', 'unknown')
        logged_in = result.get('logged_in')
        error = result.get('error')
        organized_path = result.get('organized_screenshot', 'No screenshot')
        
        if error:
            status = f"ERROR: {error[:50]}..."
        elif logged_in is True:
            status = "LOGGED IN"
        elif logged_in is False:
            status = "LOGGED OUT"
        else:
            status = "UNKNOWN"
        
        report_content += f"- {domain}: {status} | {os.path.basename(organized_path) if organized_path != 'No screenshot' else 'No screenshot'}\\n"
    
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"[i] Screenshot report generated: {report_path}")
    except Exception as e:
        print(f"[!] Failed to generate screenshot report: {e}")

def generate_html_gallery():
    """Generate an HTML gallery of all screenshots."""
    gallery_path = os.path.join(SCREENSHOTS_DIR, 'gallery.html')
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Cookie Verification Screenshot Gallery</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .section { margin-bottom: 30px; }
        .screenshot { margin: 10px; display: inline-block; text-align: center; }
        .screenshot img { max-width: 300px; max-height: 200px; border: 1px solid #ccc; }
        .screenshot p { margin: 5px 0; font-size: 12px; }
        .logged-in { border-left: 5px solid green; padding-left: 10px; }
        .logged-out { border-left: 5px solid orange; padding-left: 10px; }
        .unknown { border-left: 5px solid blue; padding-left: 10px; }
        .error { border-left: 5px solid red; padding-left: 10px; }
    </style>
</head>
<body>
    <h1>Cookie Verification Screenshot Gallery</h1>
    <p>Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
"""
    
    sections = {
        'logged_in': ('Logged In Sessions', 'logged-in'),
        'logged_out': ('Logged Out Sessions', 'logged-out'),
        'unknown': ('Unknown Status (Headless Mode)', 'unknown'),
        'errors': ('Error Screenshots', 'error')
    }
    
    for folder, (title, css_class) in sections.items():
        folder_path = os.path.join(SCREENSHOTS_DIR, folder)
        if os.path.exists(folder_path):
            screenshots = [f for f in os.listdir(folder_path) if f.endswith('.png')]
            
            html_content += f"""
    <div class="section {css_class}">
        <h2>{title} ({len(screenshots)} screenshots)</h2>
"""
            
            for screenshot in sorted(screenshots):
                screenshot_path = os.path.join(folder, screenshot)
                domain = screenshot.split('_')[1] if '_' in screenshot else 'unknown'
                
                html_content += f"""
        <div class="screenshot">
            <img src="{screenshot_path}" alt="{screenshot}" onclick="window.open(this.src)">
            <p>{domain}</p>
            <p>{screenshot}</p>
        </div>
"""
            
            html_content += "    </div>\\n"
    
    html_content += """
</body>
</html>
"""
    
    try:
        with open(gallery_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[i] HTML gallery generated: {gallery_path}")
    except Exception as e:
        print(f"[!] Failed to generate HTML gallery: {e}")

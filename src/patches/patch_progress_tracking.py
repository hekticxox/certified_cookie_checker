# ===============================
# SECTION: Progress & Focus Tracking
# ===============================
# Hooks: Auto-update progress recap and current focus based on results

import os
import datetime
from typing import List, Dict

CONTEXT_FILE = "COPILOT_CONTEXT.md"

def hook_init():
    """Initialize progress tracking system."""
    ensure_progress_sections()
    print("🔹 Progress tracking initialized.")

def hook_before_run(domain: str = None, cookies: List = None):
    """Update current focus before processing starts."""
    if domain:
        update_current_focus(f"Processing domain: {domain}")

def hook_after_run(result: Dict):
    """Update progress after each domain is processed."""
    domain = result.get('domain', 'unknown')
    success = not result.get('error')
    
    if success:
        logged_in = result.get('logged_in')
        if logged_in is True:
            update_progress_recap(f"✅ {domain}: Cookies valid, logged in session confirmed")
        elif logged_in is False:
            update_progress_recap(f"⚠️ {domain}: Cookies injected but not logged in")
        else:
            update_progress_recap(f"📸 {domain}: Screenshot taken, login status unknown (headless mode)")
    else:
        error_msg = result.get('error', 'Unknown error')
        update_progress_recap(f"❌ {domain}: Failed - {error_msg}")

def hook_cleanup(results: List, errors: List):
    """Final progress update after all processing."""
    total = len(results)
    successful = len([r for r in results if not r.get('error')])
    failed = total - successful
    
    summary = f"""
**Final Summary ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})**
- Total domains: {total}
- Successful: {successful}
- Failed: {failed}
- Success rate: {(successful/total*100):.1f}%
"""
    
    update_progress_recap(summary)
    update_current_focus("✅ Cookie verification complete")

def ensure_progress_sections():
    """Ensure progress sections exist in context file."""
    if not os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
            f.write("""# Copilot Context

## Progress Recap
Cookie verification system with automated tracking.

## Current Focus
➡️ Ready to start cookie verification

## Current Issues
(Auto-populated by error tracking)

## Resolved Issues
(Auto-populated when issues are resolved)
""")

def update_progress_recap(entry: str):
    """Add an entry to the Progress Recap section."""
    if not os.path.exists(CONTEXT_FILE):
        return
        
    with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find Progress Recap section and add entry
    lines = content.split('\\n')
    for i, line in enumerate(lines):
        if line.startswith("## Progress Recap"):
            # Insert after the header (skip the header and any existing description)
            insertion_point = i + 1
            while insertion_point < len(lines) and not lines[insertion_point].startswith("## ") and lines[insertion_point].strip():
                insertion_point += 1
            
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            lines.insert(insertion_point, f"- [{timestamp}] {entry}")
            break
    
    with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
        f.write('\\n'.join(lines))

def update_current_focus(focus: str):
    """Update the current focus section."""
    if not os.path.exists(CONTEXT_FILE):
        return
        
    with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the current focus
    lines = content.split('\\n')
    for i, line in enumerate(lines):
        if line.startswith("## Current Focus"):
            if i + 1 < len(lines):
                lines[i + 1] = f"➡️ {focus}"
            else:
                lines.append(f"➡️ {focus}")
            break
    
    with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
        f.write('\\n'.join(lines))

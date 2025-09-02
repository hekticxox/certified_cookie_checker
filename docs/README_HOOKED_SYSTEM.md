# Verified Cookie Checker - Complete Modular Hook System

## Overview
This project now includes a complete modular hook-enabled patch system that automatically logs, tracks, and analyzes your cookie verification process.

## Quick Start

```bash
# Run with full automation (headless mode)
python run_hooked_system.py

# Run with visible browser for manual verification  
python run_hooked_system.py --visible

# List all available patches
python run_hooked_system.py --list-patches
```

## System Components

### Core Files
- `verified_cookie_checker_hooked.py` - Main hook-enabled checker
- `patch_system.py` - Modular patch loading system
- `run_hooked_system.py` - Complete system launcher

### Patches (Auto-loaded)
- `patch_error_categorization.py` - Auto-categorize and log errors
- `patch_progress_tracking.py` - Auto-update progress and focus
- `patch_screenshot_analysis.py` - Organize and analyze screenshots
- `patch_smart_resume.py` - Intelligent resume and domain filtering
- `patch_auto_repair.py` - **Self-healing system with auto-fixes**
- `patch_enhanced_recovery.py` - **Advanced retry logic and escalation**

## Features

### 🔍 Automatic Error Categorization
- Detects and categorizes common errors
- Suggests fixes (missing packages, driver issues, etc.)
- Logs all errors to `error_log.json`
- Updates `COPILOT_CONTEXT.md` with current issues

### 📊 Progress Tracking  
- Real-time progress updates in `COPILOT_CONTEXT.md`
- Automatic current focus updates
- Session statistics and success rates
- Timestamped progress entries

### 📸 Screenshot Organization
- Automatically organizes screenshots by status:
  - `screenshots_organized/logged_in/` - Successful logins
  - `screenshots_organized/logged_out/` - Logged out sessions  
  - `screenshots_organized/unknown/` - Headless mode results
  - `screenshots_organized/errors/` - Failed attempts
- Generates HTML gallery (`gallery.html`)
- Detailed screenshot reports

### 🧠 Smart Resume System
- Tracks recently failed domains (24h retry delay)
- Auto-adds repeatedly failing domains to skip list
- Domain filtering and pattern matching
- Intelligent recommendations based on results

### 🔧 Auto-Repair System (NEW!)
- **Self-healing**: Automatically detects and fixes common issues
- **ChromeDriver fixes**: Auto-downloads and configures ChromeDriver
- **Package installation**: Auto-installs missing Python packages
- **Permission fixes**: Resolves file access and permission issues
- **Chrome cleanup**: Kills hanging processes and clears cache
- **Space management**: Automatically cleans old logs and screenshots

### 🔄 Enhanced Error Recovery (NEW!)
- **Smart retry logic**: Exponential backoff for failed domains
- **Error categorization**: Identifies timeout, network, webdriver issues
- **Preemptive fixes**: Applies fixes before retrying based on error patterns
- **Escalation strategies**: Manual review queue and permanent skip lists
- **Recovery tracking**: Detailed logs of all repair attempts

## Generated Reports

After running, you'll get these auto-generated files:

1. **COPILOT_CONTEXT.md** - Live progress tracking
2. **error_log.json** - Detailed error categorization  
3. **screenshots_organized/** - Organized screenshot folders
4. **screenshots_organized/gallery.html** - Visual gallery
5. **resume_state.json** - Smart resume data
6. **domain_filters.json** - Domain filtering config
7. **VerifiedCookies.json** - Complete results
8. **auto_repair.json** - **Self-healing repair logs and success rates**
9. **retry_state.json** - **Enhanced retry tracking and escalation data**
10. **manual_review_queue.json** - **Domains flagged for manual review**

## Hook System

The patch system uses hooks that automatically trigger:

- `hook_init()` - Run once at startup
- `hook_before_run(domain, cookies)` - Before processing each domain
- `hook_after_run(result)` - After processing each domain  
- `hook_on_error(error_message, domain)` - When errors occur
- `hook_on_success(result)` - When processing succeeds
- `hook_cleanup(results, errors)` - Final cleanup and reports

## Adding Custom Patches

Create `patches/patch_your_feature.py`:

```python
# ===============================
# SECTION: Your Custom Feature
# ===============================

def hook_init():
    """Initialize your feature."""
    print("🔹 Custom feature initialized.")

def hook_after_run(result):
    """Process each result."""
    domain = result.get('domain')
    # Your custom logic here
    
def hook_cleanup(results, errors):
    """Final processing."""
    # Generate custom reports
```

The patch will be automatically loaded and executed!

## Example Output

```
🚀 HOOK-ENABLED VERIFIED COOKIE CHECKER
════════════════════════════════════════════════════════════
🔹 Error tracking system initialized.
🔹 Progress tracking initialized.  
🔹 Screenshot organization system initialized.
🔹 Smart resume system initialized.
🔹 Auto-repair system initialized - self-healing enabled.
🔹 Enhanced error recovery system initialized.

[i] Launching headless Chrome for domain: .adobe.com
[i] Injected cookie: session_id for .adobe.com
📸 Screenshot saved: adobe.com_screenshot.png
🔹 Auto-logged progress: ✅ .adobe.com: Screenshot taken

❌ Error detected: ChromeDriver not found
🔧 Auto-repair applied for error: ChromeDriver not found...
🔄 Retrying operation...
✅ Successfully installed ChromeDriver

🔄 RETRY STATE SUMMARY:
   Active retry schedules: 2
   Exhausted retries: 1

🔧 AUTO-REPAIR SUMMARY:
   Total repairs attempted: 5
   Success rate: 80.0%
   Recent repair types:
     - chromedriver_fix: 2
     - package_install: 1

📋 GENERATED REPORTS:
═══════════════════════════════════════════════════════════
✅ COPILOT_CONTEXT.md - Progress tracking and current focus
✅ screenshots_organized/ - Organized screenshots by status  
✅ resume_state.json - Smart resume and domain analysis
✅ auto_repair.json - Self-healing repair logs and success rates
🎉 All done! Check the generated reports for detailed analysis.
```

## Benefits

- **Zero Manual Logging**: Everything is tracked automatically
- **Smart Error Handling**: Errors are categorized with actionable suggestions  
- **Visual Organization**: Screenshots sorted by login status
- **Intelligent Resume**: Skip problematic domains, retry smart
- **Complete Audit Trail**: Every action logged with timestamps
- **Modular & Extensible**: Add new features without touching core code
- **🔧 Self-Healing**: Automatically fixes common issues without user intervention
- **🔄 Auto-Recovery**: Smart retry logic with exponential backoff and escalation
- **📊 Repair Tracking**: Detailed logs of all auto-repair attempts and success rates

This system transforms your cookie checker into a fully automated, self-documenting, **self-healing** verification pipeline!

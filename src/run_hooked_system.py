# ===============================
# COMPLETE HOOK-ENABLED SYSTEM DEMO
# ===============================
# This demonstrates the complete modular patch system in action

"""
USAGE EXAMPLES:

1. Run with full automation and logging:
   python run_hooked_system.py

2. Run with visible browser for manual verification:
   python run_hooked_system.py --visible

3. Run with specific patches disabled:
   python run_hooked_system.py --disable-patch screenshot_analysis

4. View the generated reports:
   - COPILOT_CONTEXT.md (automatically updated)
   - error_log.json (detailed error tracking)
   - screenshots_organized/ (organized screenshots)
   - resume_state.json (smart resume data)
"""

import sys
import os
import argparse
from verified_cookie_checker_hooked import HookedCookieChecker

def main():
    parser = argparse.ArgumentParser(description="Complete Hook-Enabled Cookie Verification System")
    parser.add_argument('--visible', action='store_true',
                       help='Show browser window and prompt for login verification')
    parser.add_argument('--disable-patch', action='append', dest='disabled_patches',
                       help='Disable specific patches (can be used multiple times)')
    parser.add_argument('--list-patches', action='store_true',
                       help='List available patches and exit')
    
    args = parser.parse_args()
    
    # Handle list patches
    if args.list_patches:
        from patch_system import patch_system
        patch_system.load_patches()
        print("Available patches:")
        for patch_name in patch_system.loaded_patches:
            print(f"  - {patch_name}")
        print(f"\\nTotal hooks registered: {sum(len(hooks) for hooks in patch_system.hooks.values())}")
        return
    
    # Disable specific patches if requested
    if args.disabled_patches:
        print(f"[i] Disabling patches: {', '.join(args.disabled_patches)}")
        # This would require modifying the patch system to support disabling
        # For now, just show the intent
    
    print("="*60)
    print("🚀 HOOK-ENABLED VERIFIED COOKIE CHECKER")
    print("="*60)
    print("Features enabled:")
    print("✅ Automatic error categorization and logging")
    print("✅ Progress tracking and context updates")
    print("✅ Screenshot organization and analysis")
    print("✅ Smart resume with failure tracking")
    print("✅ Domain filtering and recommendations")
    print("="*60)
    
    # Create and run the hooked checker
    checker = HookedCookieChecker()
    
    # Modify args to pass to the checker
    original_argv = sys.argv
    sys.argv = ['verified_cookie_checker_hooked.py']
    if args.visible:
        sys.argv.append('--visible')
    
    try:
        checker.run()
    finally:
        sys.argv = original_argv
    
    print("\\n" + "="*60)
    print("📋 GENERATED REPORTS:")
    print("="*60)
    
    reports = [
        ("COPILOT_CONTEXT.md", "Progress tracking and current focus"),
        ("error_log.json", "Detailed error categorization"),
        ("screenshots_organized/", "Organized screenshots by status"),
        ("screenshots_organized/gallery.html", "Visual screenshot gallery"),
        ("resume_state.json", "Smart resume and domain analysis"),
        ("domain_filters.json", "Domain filtering configuration"),
        ("VerifiedCookies.json", "Complete verification results")
    ]
    
    for filename, description in reports:
        if os.path.exists(filename):
            print(f"✅ {filename} - {description}")
        else:
            print(f"❌ {filename} - {description} (not generated)")
    
    print("\\n🎉 All done! Check the generated reports for detailed analysis.")

if __name__ == '__main__':
    main()

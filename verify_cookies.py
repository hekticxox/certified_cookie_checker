#!/usr/bin/env python3
"""
Cookie Verification System - Main Launcher
Handles the new directory structure with personal/ separation
"""

import os
import sys
import argparse
from pathlib import Path

# Add src directory to Python path
SCRIPT_DIR = Path(__file__).parent
SRC_DIR = SCRIPT_DIR / "src"
PERSONAL_DIR = SCRIPT_DIR / "personal"

sys.path.insert(0, str(SRC_DIR))

def ensure_personal_structure():
    """Ensure personal directory structure exists"""
    dirs = [
        PERSONAL_DIR / "cookies",
        PERSONAL_DIR / "logs", 
        PERSONAL_DIR / "screenshots",
        PERSONAL_DIR / "state"
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        
    # Create .gitkeep files to maintain structure
    for dir_path in dirs:
        gitkeep = dir_path / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()

def main():
    parser = argparse.ArgumentParser(description="Cookie Verification System")
    parser.add_argument("--cookies", help="Path to cookies file (relative to personal/cookies/)")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--visible", action="store_true", help="Run with visible browser")
    parser.add_argument("--monitor", action="store_true", help="Run system monitor instead")
    parser.add_argument("--setup", action="store_true", help="Run production setup")
    
    args = parser.parse_args()
    
    # Ensure directory structure
    ensure_personal_structure()
    
    if args.setup:
        # Run setup from src directory
        os.chdir(SRC_DIR)
        import setup_production
        return
        
    if args.monitor:
        # Run monitor from src directory  
        os.chdir(SRC_DIR)
        import system_monitor
        return
    
    # Change to project root for main execution
    os.chdir(SCRIPT_DIR)
    
    # Import and run the hooked system
    from src.run_hooked_system import main as run_main
    
    # Adjust cookie path if provided
    if args.cookies:
        # If path doesn't exist as-is, try relative to personal/cookies/
        if not os.path.exists(args.cookies):
            personal_path = PERSONAL_DIR / "cookies" / args.cookies
            if personal_path.exists():
                args.cookies = str(personal_path)
    
    # Set up arguments for the main system
    sys.argv = ["run_hooked_system.py"]
    if args.cookies:
        sys.argv.extend(["--cookies", args.cookies])
    if args.headless:
        sys.argv.append("--headless")
    if args.visible:
        sys.argv.append("--visible")
        
    run_main()

if __name__ == "__main__":
    main()

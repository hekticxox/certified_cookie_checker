# 📂 Workspace Organization Guide

This repository is now properly organized for both development and production use.

## 🗂️ Directory Structure

### Production Code (`src/`)
- Contains all the core verification system
- Gets pushed to git and shared with users
- Should be stable and well-tested

### Personal Working Files (`personal/`)
- **NEVER pushed to git** - your private workspace
- Contains your actual cookie files, logs, screenshots
- Organized into subdirectories for easy management

### Documentation (`docs/`)
- Comprehensive guides and API documentation
- Gets pushed to git for users

### Examples (`examples/`)
- Sample files and configuration templates
- Safe examples that don't contain real data
- Gets pushed to git to help users

## 🚀 Usage Patterns

### For Development:
```bash
# Use the main launcher (handles paths automatically)
python verify_cookies.py --cookies my_cookies.txt --headless

# Or use the batch file
verify.bat

# Monitor running processes
verify.bat monitor

# Set up environment
verify.bat setup
```

### For Production/Users:
```bash
# Clone and set up
git clone [your-repo]
cd VERIFIEDCOOKIECHECKER
python verify_cookies.py --setup

# Add cookies to personal/cookies/
# Run verification
python verify_cookies.py --cookies your_cookies.txt
```

## 🔒 Privacy Benefits

1. **Clean Git History**: No accidental commits of personal data
2. **Safe Sharing**: Repository can be shared without exposing cookies/logs
3. **Organized Workflow**: Clear separation between code and data
4. **Easy Cleanup**: Personal directory can be deleted/ignored safely

## 📝 Best Practices

1. Put all cookie files in `personal/cookies/`
2. Check `personal/logs/` for verification results
3. Review `personal/screenshots/` for visual confirmation
4. Back up `personal/state/` for resume functionality
5. Never manually edit files in `src/` unless you know what you're doing

This organization makes the repository both professional and user-friendly!

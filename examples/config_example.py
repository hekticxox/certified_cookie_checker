# Configuration Example
# Copy this to personal/ directory and customize for your needs

import os

# Personal working directories (not pushed to git)
PERSONAL_DIR = "personal"
COOKIES_DIR = os.path.join(PERSONAL_DIR, "cookies")
LOGS_DIR = os.path.join(PERSONAL_DIR, "logs") 
SCREENSHOTS_DIR = os.path.join(PERSONAL_DIR, "screenshots")
STATE_DIR = os.path.join(PERSONAL_DIR, "state")

# Your personal cookie files
COOKIE_FILES = [
    os.path.join(COOKIES_DIR, "my_cookies.txt"),
    # Add more cookie files as needed
]

# Custom domain filters
SKIP_DOMAINS = [
    "problematic-domain.com",
    # Add domains you want to skip
]

# Browser settings
HEADLESS_MODE = True  # Set to False for debugging
SCREENSHOT_ON_ERROR = True
TIMEOUT_SECONDS = 30

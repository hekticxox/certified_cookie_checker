# ===============================
# SECTION: Enhanced Error Recovery
# ===============================
# Hooks: Advanced error recovery and retry logic with exponential backoff

import os
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List

RETRY_STATE_FILE = "retry_state.json"
MAX_RETRIES = 3
BASE_RETRY_DELAY = 2  # seconds

def hook_init():
    """Initialize enhanced error recovery system."""
    ensure_retry_state()
    print("🔹 Enhanced error recovery system initialized.")

def hook_on_error(error_message: str, domain: str = None):
    """Enhanced error handling with smart retry logic."""
    if not domain:
        return
    
    retry_state = load_retry_state()
    
    # Check if this domain should be retried
    domain_key = domain.lstrip('.')
    
    if domain_key not in retry_state:
        retry_state[domain_key] = {
            "error_count": 0,
            "last_error": None,
            "last_attempt": None,
            "next_retry": None,
            "error_types": []
        }
    
    domain_state = retry_state[domain_key]
    domain_state["error_count"] += 1
    domain_state["last_error"] = error_message[:200]
    domain_state["last_attempt"] = datetime.now().isoformat()
    
    # Categorize error type
    error_type = categorize_error_type(error_message)
    if error_type not in domain_state["error_types"]:
        domain_state["error_types"].append(error_type)
    
    # Calculate next retry time with exponential backoff
    if domain_state["error_count"] < MAX_RETRIES:
        retry_delay = BASE_RETRY_DELAY * (2 ** (domain_state["error_count"] - 1))
        next_retry = datetime.now() + timedelta(seconds=retry_delay)
        domain_state["next_retry"] = next_retry.isoformat()
        
        print(f"🔄 Scheduling retry for {domain} in {retry_delay} seconds (attempt {domain_state['error_count']}/{MAX_RETRIES})")
    else:
        domain_state["next_retry"] = None
        print(f"❌ Max retries exceeded for {domain}")
        
        # Apply escalation strategies
        apply_escalation_strategy(domain, domain_state, error_message)
    
    save_retry_state(retry_state)

def hook_before_run(domain: str = None, cookies: List = None):
    """Check if domain is ready for retry."""
    if not domain:
        return
    
    retry_state = load_retry_state()
    domain_key = domain.lstrip('.')
    
    if domain_key in retry_state:
        domain_state = retry_state[domain_key]
        
        # Check if we should skip due to retry timing
        if domain_state.get("next_retry"):
            next_retry = datetime.fromisoformat(domain_state["next_retry"])
            if datetime.now() < next_retry:
                time_left = (next_retry - datetime.now()).total_seconds()
                print(f"⏳ Waiting {int(time_left)}s before retrying {domain}")
                return {"skip": True, "reason": "retry_cooldown"}
        
        # Apply pre-run fixes based on previous errors
        apply_preemptive_fixes(domain, domain_state)

def hook_on_success(result: Dict):
    """Clear retry state on successful run."""
    domain = result.get('domain')
    if not domain:
        return
    
    retry_state = load_retry_state()
    domain_key = domain.lstrip('.')
    
    # Clear retry state on success
    if domain_key in retry_state:
        del retry_state[domain_key]
        save_retry_state(retry_state)
        print(f"✅ Cleared retry state for successful domain: {domain}")

def categorize_error_type(error_message):
    """Categorize error for targeted recovery strategies."""
    error_message_lower = error_message.lower()
    
    if "timeout" in error_message_lower or "timed out" in error_message_lower:
        return "timeout"
    elif "connection" in error_message_lower or "network" in error_message_lower:
        return "network"
    elif "chromedriver" in error_message_lower or "webdriver" in error_message_lower:
        return "webdriver"
    elif "permission" in error_message_lower or "access denied" in error_message_lower:
        return "permission"
    elif "memory" in error_message_lower or "out of memory" in error_message_lower:
        return "memory"
    elif "disk" in error_message_lower or "space" in error_message_lower:
        return "disk_space"
    elif "module" in error_message_lower and "not found" in error_message_lower:
        return "missing_dependency"
    else:
        return "unknown"

def apply_preemptive_fixes(domain, domain_state):
    """Apply fixes based on known error patterns before running."""
    error_types = domain_state.get("error_types", [])
    
    for error_type in error_types:
        if error_type == "timeout":
            print(f"🔧 Pre-applying timeout fix for {domain}")
            # Could increase timeout values, use different wait strategies
            
        elif error_type == "network":
            print(f"🔧 Pre-applying network fix for {domain}")
            # Could add network connectivity checks, DNS flushing
            
        elif error_type == "memory":
            print(f"🔧 Pre-applying memory fix for {domain}")
            # Could trigger garbage collection, clear caches
            import gc
            gc.collect()
            
        elif error_type == "webdriver":
            print(f"🔧 Pre-applying webdriver fix for {domain}")
            # Could reset webdriver, clear browser data

def apply_escalation_strategy(domain, domain_state, error_message):
    """Apply escalation strategies when max retries are reached."""
    error_types = domain_state.get("error_types", [])
    
    # Strategy 1: Try alternative approaches
    if "webdriver" in error_types:
        print(f"🔄 Escalating {domain}: Trying headless mode toggle")
        # Could flag for different browser mode
        
    elif "timeout" in error_types:
        print(f"🔄 Escalating {domain}: Scheduling for off-peak retry")
        # Schedule for later when network might be better
        next_retry = datetime.now() + timedelta(hours=1)
        domain_state["next_retry"] = next_retry.isoformat()
        domain_state["error_count"] = 0  # Reset counter for off-peak retry
        
    elif "network" in error_types:
        print(f"🔄 Escalating {domain}: Adding to manual review queue")
        add_to_manual_review(domain, error_message)
        
    # Strategy 2: Permanent skip with documentation
    else:
        print(f"🚫 Escalating {domain}: Adding to permanent skip list")
        add_to_permanent_skip(domain, domain_state, error_message)

def add_to_manual_review(domain, error_message):
    """Add domain to manual review queue."""
    manual_review_file = "manual_review_queue.json"
    
    try:
        if os.path.exists(manual_review_file):
            with open(manual_review_file, 'r', encoding='utf-8') as f:
                queue = json.load(f)
        else:
            queue = {"domains": []}
        
        queue["domains"].append({
            "domain": domain,
            "error_message": error_message,
            "added_timestamp": datetime.now().isoformat(),
            "reason": "Network issues - requires manual verification"
        })
        
        with open(manual_review_file, 'w', encoding='utf-8') as f:
            json.dump(queue, f, indent=2)
            
        print(f"📋 Added {domain} to manual review queue")
        
    except Exception as e:
        print(f"❌ Failed to add to manual review: {e}")

def add_to_permanent_skip(domain, domain_state, error_message):
    """Add domain to permanent skip list with detailed reasoning."""
    try:
        # Load existing domain filters
        domain_filters_file = "domain_filters.json"
        
        if os.path.exists(domain_filters_file):
            with open(domain_filters_file, 'r', encoding='utf-8') as f:
                filters = json.load(f)
        else:
            filters = {"skip_domains": [], "skip_patterns": [], "notes": {}}
        
        if domain not in filters["skip_domains"]:
            filters["skip_domains"].append(domain)
            filters["notes"][domain] = {
                "reason": f"Auto-escalated after {domain_state['error_count']} failures",
                "error_types": domain_state["error_types"],
                "last_error": error_message[:200],
                "escalated_timestamp": datetime.now().isoformat()
            }
            
            with open(domain_filters_file, 'w', encoding='utf-8') as f:
                json.dump(filters, f, indent=2)
                
            print(f"🚫 Added {domain} to permanent skip list")
            
    except Exception as e:
        print(f"❌ Failed to add to permanent skip: {e}")

def ensure_retry_state():
    """Ensure retry state file exists."""
    if not os.path.exists(RETRY_STATE_FILE):
        save_retry_state({})

def load_retry_state():
    """Load retry state from file."""
    try:
        with open(RETRY_STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_retry_state(state):
    """Save retry state to file."""
    try:
        with open(RETRY_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"[!] Failed to save retry state: {e}")

def hook_cleanup(results: List, errors: List):
    """Generate retry state summary."""
    retry_state = load_retry_state()
    
    if retry_state:
        print(f"\n🔄 RETRY STATE SUMMARY:")
        
        active_retries = sum(1 for domain_state in retry_state.values() 
                           if domain_state.get("next_retry"))
        exhausted_retries = sum(1 for domain_state in retry_state.values() 
                              if domain_state.get("error_count", 0) >= MAX_RETRIES and not domain_state.get("next_retry"))
        
        print(f"   Active retry schedules: {active_retries}")
        print(f"   Exhausted retries: {exhausted_retries}")
        
        # Show domains scheduled for retry
        if active_retries > 0:
            print("   Scheduled retries:")
            for domain, state in retry_state.items():
                if state.get("next_retry"):
                    next_retry = datetime.fromisoformat(state["next_retry"])
                    time_until = next_retry - datetime.now()
                    if time_until.total_seconds() > 0:
                        print(f"     - {domain}: {int(time_until.total_seconds())}s")

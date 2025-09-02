# ===============================
# SECTION: Smart Resume & Domain Filtering
# ===============================
# Hooks: Intelligent resume functionality and domain filtering

import os
import json
from typing import Dict, List, Set
from datetime import datetime, timedelta

RESUME_STATE_FILE = "resume_state.json"
DOMAIN_FILTERS_FILE = "domain_filters.json"

def hook_init():
    """Initialize smart resume system."""
    ensure_resume_state()
    ensure_domain_filters()
    print("🔹 Smart resume system initialized.")

def hook_before_run(domain: str = None, cookies: List = None):
    """Check if domain should be skipped based on filters or recent results."""
    if not domain:
        return
    
    # Load domain filters
    filters = load_domain_filters()
    
    # Check if domain is in skip list
    if domain in filters.get('skip_domains', []):
        print(f"[i] Skipping {domain} (in skip list)")
        return {'skip': True}
    
    # Check if domain matches skip patterns
    for pattern in filters.get('skip_patterns', []):
        if pattern in domain:
            print(f"[i] Skipping {domain} (matches pattern: {pattern})")
            return {'skip': True}
    
    # Check recent failures
    state = load_resume_state()
    recent_failures = state.get('recent_failures', {})
    
    if domain in recent_failures:
        last_failure = datetime.fromisoformat(recent_failures[domain])
        if datetime.now() - last_failure < timedelta(hours=24):
            print(f"[i] Skipping {domain} (failed recently, retry after 24h)")
            return {'skip': True}

def hook_on_error(error_message: str, domain: str = None):
    """Track failed domains for smart retry logic."""
    if domain:
        state = load_resume_state()
        if 'recent_failures' not in state:
            state['recent_failures'] = {}
        
        state['recent_failures'][domain] = datetime.now().isoformat()
        save_resume_state(state)
        
        # Auto-add to skip list if it fails repeatedly
        failure_count = state.get('failure_counts', {}).get(domain, 0) + 1
        if 'failure_counts' not in state:
            state['failure_counts'] = {}
        state['failure_counts'][domain] = failure_count
        
        if failure_count >= 3:
            add_to_skip_list(domain, f"Failed {failure_count} times")

def hook_on_success(result: Dict):
    """Clean up successful domains from failure tracking."""
    domain = result.get('domain')
    if not domain:
        return
        
    state = load_resume_state()
    
    # Remove from recent failures
    if 'recent_failures' in state and domain in state['recent_failures']:
        del state['recent_failures'][domain]
    
    # Reset failure count
    if 'failure_counts' in state and domain in state['failure_counts']:
        del state['failure_counts'][domain]
    
    # Add to successful domains
    if 'successful_domains' not in state:
        state['successful_domains'] = {}
    
    state['successful_domains'][domain] = {
        'timestamp': datetime.now().isoformat(),
        'logged_in': result.get('logged_in'),
        'cookies_injected': result.get('cookies_injected', 0)
    }
    
    save_resume_state(state)

def hook_cleanup(results: List, errors: List):
    """Update resume state and generate domain analysis."""
    state = load_resume_state()
    
    # Update session statistics
    state['last_session'] = {
        'timestamp': datetime.now().isoformat(),
        'total_domains': len(results),
        'successful': len([r for r in results if not r.get('error')]),
        'failed': len([r for r in results if r.get('error')])
    }
    
    # Generate domain recommendations
    recommendations = generate_domain_recommendations(results)
    state['recommendations'] = recommendations
    
    save_resume_state(state)
    print_domain_analysis(recommendations)

def ensure_resume_state():
    """Ensure resume state file exists."""
    if not os.path.exists(RESUME_STATE_FILE):
        initial_state = {
            'recent_failures': {},
            'failure_counts': {},
            'successful_domains': {},
            'last_session': None,
            'recommendations': {}
        }
        save_resume_state(initial_state)

def ensure_domain_filters():
    """Ensure domain filters file exists."""
    if not os.path.exists(DOMAIN_FILTERS_FILE):
        initial_filters = {
            'skip_domains': [],
            'skip_patterns': [],
            'priority_domains': [],
            'notes': {}
        }
        save_domain_filters(initial_filters)

def load_resume_state():
    """Load resume state from file."""
    try:
        with open(RESUME_STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_resume_state(state):
    """Save resume state to file."""
    try:
        with open(RESUME_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"[!] Failed to save resume state: {e}")

def load_domain_filters():
    """Load domain filters from file."""
    try:
        with open(DOMAIN_FILTERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {'skip_domains': [], 'skip_patterns': [], 'priority_domains': [], 'notes': {}}

def save_domain_filters(filters):
    """Save domain filters to file."""
    try:
        with open(DOMAIN_FILTERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(filters, f, indent=2)
    except Exception as e:
        print(f"[!] Failed to save domain filters: {e}")

def add_to_skip_list(domain: str, reason: str = "Manual"):
    """Add domain to skip list."""
    filters = load_domain_filters()
    if domain not in filters['skip_domains']:
        filters['skip_domains'].append(domain)
        filters['notes'][domain] = f"Added: {datetime.now().isoformat()} - {reason}"
        save_domain_filters(filters)
        print(f"[i] Added {domain} to skip list: {reason}")

def generate_domain_recommendations(results: List) -> Dict:
    """Generate recommendations based on results."""
    recommendations = {
        'high_value_domains': [],
        'problematic_domains': [],
        'unknown_status_domains': []
    }
    
    for result in results:
        domain = result.get('domain')
        if not domain:
            continue
            
        if result.get('logged_in') is True:
            recommendations['high_value_domains'].append({
                'domain': domain,
                'reason': 'Successfully logged in',
                'cookies_count': len(result.get('cookies', []))
            })
        elif result.get('error'):
            recommendations['problematic_domains'].append({
                'domain': domain,
                'error': result.get('error'),
                'suggestion': 'Consider adding to skip list or investigating'
            })
        elif result.get('logged_in') is None:
            recommendations['unknown_status_domains'].append({
                'domain': domain,
                'reason': 'Headless mode - consider manual verification',
                'screenshot': result.get('screenshot')
            })
    
    return recommendations

def print_domain_analysis(recommendations: Dict):
    """Print domain analysis to console."""
    print("\\n" + "="*50)
    print("DOMAIN ANALYSIS")
    print("="*50)
    
    high_value = recommendations.get('high_value_domains', [])
    if high_value:
        print(f"\\n🎯 HIGH VALUE DOMAINS ({len(high_value)}):")
        for domain_info in high_value:
            print(f"  - {domain_info['domain']}: {domain_info['reason']}")
    
    problematic = recommendations.get('problematic_domains', [])
    if problematic:
        print(f"\\n⚠️ PROBLEMATIC DOMAINS ({len(problematic)}):")
        for domain_info in problematic:
            print(f"  - {domain_info['domain']}: {domain_info['error'][:60]}...")
    
    unknown = recommendations.get('unknown_status_domains', [])
    if unknown:
        print(f"\\n❓ UNKNOWN STATUS DOMAINS ({len(unknown)}):")
        for domain_info in unknown:
            print(f"  - {domain_info['domain']}: Consider manual verification")
    
    print("\\n" + "="*50)

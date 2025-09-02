# ===============================
# HOOK-ENABLED VERIFIED COOKIE CHECKER
# ===============================
# Main script that integrates with the patch system for auto-logging and tracking

import os
import sys
import json
import time
import argparse
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

# Import the patch system
try:
    from patch_system import patch_system
    PATCH_SYSTEM_AVAILABLE = True
except ImportError:
    PATCH_SYSTEM_AVAILABLE = False
    print("[!] Patch system not available. Running without hooks.")

class HookedCookieChecker:
    def __init__(self):
        self.results = []
        self.errors = []
        
        if PATCH_SYSTEM_AVAILABLE:
            # Load all patches
            patch_system.load_patches()
            # Execute initialization hooks
            patch_system.execute_hooks('init')
    
    def get_directory(self):
        """Prompt the user to enter a valid directory path containing cookie files."""
        while True:
            path = input('Enter the path to the directory containing cookie files: ').strip()
            if os.path.isdir(path):
                return path
            print('Invalid directory. Please try again.')

    def list_cookie_files(self, dir_path):
        """List all .txt files in the directory."""
        files = [f for f in os.listdir(dir_path) if f.endswith('.txt')]
        return files

    def parse_netscape_cookie_line(self, line):
        """Parse a single Netscape-format cookie line."""
        parts = line.strip().split('\t')
        if len(parts) != 7:
            return None
        domain, flag, path, secure, expiration, name, value = parts
        try:
            expiration = int(expiration)
        except ValueError:
            return None
        return {
            'domain': domain,
            'flag': flag,
            'path': path,
            'secure': secure.upper() == 'TRUE',
            'expiration': expiration,
            'name': name,
            'value': value
        }

    def parse_cookies(self, cookies_path):
        """Parse cookies from a Netscape-format file, filtering out expired ones."""
        cookies_by_domain = {}
        now = int(time.time())
        try:
            with open(cookies_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('#') or not line.strip():
                        continue
                    cookie = self.parse_netscape_cookie_line(line)
                    if cookie and cookie['expiration'] > now:
                        cookies_by_domain.setdefault(cookie['domain'], []).append(cookie)
            return cookies_by_domain
        except Exception as e:
            error_msg = f"Failed to parse cookies from {cookies_path}: {e}"
            self.handle_error(error_msg)
            return {}

    def get_test_url(self, domain, autofill_domains):
        """Generate test URL for a domain."""
        if domain in autofill_domains:
            return autofill_domains[domain]
        return f'https://{domain.lstrip(".")}/'

    def test_cookie_session(self, domain, cookies, url, screenshot_dir=None, visible=False):
        """
        Launch Chrome (headless or visible), inject cookies, take a screenshot, and log results.
        Returns a dictionary with results.
        """
        if PATCH_SYSTEM_AVAILABLE:
            # Execute before_run hooks
            patch_system.execute_hooks('before_run', domain=domain, cookies=cookies)
        
        options = Options()
        if not visible:
            options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        if visible:
            options.add_argument('--start-maximized')
        headless = not visible

        log_file = os.path.join(screenshot_dir or ".", f"{domain.lstrip('.')}_chromedriver.log")
        service = Service(log_path=log_file)
        if os.name == 'nt':
            service.creation_flags = subprocess.CREATE_NO_WINDOW

        driver = None
        result = {
            'domain': domain,
            'url': url,
            'cookies': cookies,
            'logged_in': None,
            'screenshot': None,
            'log_file': log_file,
            'error': None
        }

        try:
            mode = "visible" if visible else "headless"
            print(f"[i] Launching {mode} Chrome for domain: {domain}")
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url)
            driver.delete_all_cookies()
            
            cookie_success_count = 0
            for cookie in cookies:
                cookie_dict = {
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': cookie['domain'],
                    'path': cookie['path'],
                    'secure': cookie['secure'],
                    'expiry': cookie['expiration']
                }
                try:
                    driver.add_cookie(cookie_dict)
                    print(f"[i] Injected cookie: {cookie['name']} for {domain}")
                    cookie_success_count += 1
                except WebDriverException as e:
                    error_msg = f"Failed to inject cookie: {cookie['name']} for {domain}"
                    print(f"[!] {error_msg}")
                    self.handle_error(f"{error_msg}: {str(e)}", domain)
            
            driver.refresh()
            time.sleep(5)
            
            if screenshot_dir:
                screenshot_path = os.path.join(screenshot_dir, f"{domain.lstrip('.')}_screenshot.png")
                driver.save_screenshot(screenshot_path)
                result['screenshot'] = screenshot_path
                print(f"[i] Screenshot saved: {screenshot_path}")
            
            # Only prompt if not headless
            if not headless:
                while True:
                    ans = input(f'Is this a logged-in session for {domain}? (y/n): ').strip().lower()
                    if ans in ('y', 'n'):
                        result['logged_in'] = (ans == 'y')
                        break
                    print("Please enter 'y' or 'n'.")
            else:
                result['logged_in'] = None
                
            result['cookies_injected'] = cookie_success_count
            
            if PATCH_SYSTEM_AVAILABLE:
                # Execute success hooks
                patch_system.execute_hooks('on_success', result=result)
                
        except Exception as e:
            error_msg = f"Error testing cookies for {domain}: {str(e)}"
            result['error'] = error_msg
            self.handle_error(error_msg, domain)
            
        finally:
            if driver:
                driver.quit()
                
            if PATCH_SYSTEM_AVAILABLE:
                # Execute after_run hooks
                patch_system.execute_hooks('after_run', result=result)
        
        return result

    def handle_error(self, error_message, domain=None):
        """Handle errors with patch system integration."""
        self.errors.append({'message': error_message, 'domain': domain})
        
        if PATCH_SYSTEM_AVAILABLE:
            # Execute error hooks
            patch_system.execute_hooks('on_error', error_message=error_message, domain=domain)
        else:
            print(f"[!] {error_message}")

    def log_results(self, results, out_path):
        """Write JSON results to a file."""
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            print(f"[i] Results written to {out_path}")
        except Exception as e:
            self.handle_error(f"Failed to write results to {out_path}: {str(e)}")

    def run(self):
        """Main execution method."""
        parser = argparse.ArgumentParser(description="Hook-Enabled Verified Cookie Checker")
        parser.add_argument('--visible', action='store_true', 
                          help='Show browser window and prompt for login verification')
        args = parser.parse_args()

        dir_path = self.get_directory()
        cookie_files = self.list_cookie_files(dir_path)

        if not cookie_files:
            error_msg = "No .txt cookie files found in directory."
            self.handle_error(error_msg)
            sys.exit(1)

        # Prompt user to select a file or ALL
        print("Multiple .txt files found. Select which one to use (or type 'ALL'):")
        for i, f in enumerate(cookie_files, 1):
            print(f"{i}. {f}")

        choice = input(f"Enter the number (1-{len(cookie_files)}) or 'ALL': ").strip()
        selected_files = []
        if choice.lower() == 'all':
            selected_files = cookie_files
        elif choice.isdigit() and 1 <= int(choice) <= len(cookie_files):
            selected_files = [cookie_files[int(choice)-1]]
        else:
            error_msg = "Invalid choice. Exiting."
            self.handle_error(error_msg)
            sys.exit(1)

        out_path = os.path.join(dir_path, 'VerifiedCookies.json')
        screenshot_dir = dir_path

        # Load previous results if exist
        if os.path.exists(out_path):
            try:
                with open(out_path, 'r', encoding='utf-8') as f:
                    all_results = json.load(f)
                # Track domains already checked
                checked_domains = {r['domain'] for r in all_results}
            except Exception as e:
                self.handle_error(f"Failed to load existing results: {str(e)}")
                all_results = []
                checked_domains = set()
        else:
            all_results = []
            checked_domains = set()

        # Process each selected file
        for cookie_file in selected_files:
            cookies_path = os.path.join(dir_path, cookie_file)
            cookies_by_domain = self.parse_cookies(cookies_path)

            for domain, cookies in cookies_by_domain.items():
                if domain in checked_domains:
                    print(f"[i] Skipping {domain}, already checked.")
                    continue

                url = self.get_test_url(domain, {})
                result = self.test_cookie_session(domain, cookies, url, 
                                               screenshot_dir=screenshot_dir, visible=args.visible)
                all_results.append(result)
                self.results.append(result)
                self.log_results(all_results, out_path)

        # Final summary
        total_domains = len(self.results)
        successful_domains = len([r for r in self.results if not r.get('error')])
        failed_domains = total_domains - successful_domains
        
        print(f"\n[i] Processing complete!")
        print(f"[i] Total domains processed: {total_domains}")
        print(f"[i] Successful: {successful_domains}")
        print(f"[i] Failed: {failed_domains}")
        print(f"[i] All results written to {out_path}")
        
        if PATCH_SYSTEM_AVAILABLE:
            # Execute cleanup hooks
            patch_system.execute_hooks('cleanup', results=self.results, errors=self.errors)

def main():
    """Entry point."""
    checker = HookedCookieChecker()
    checker.run()

if __name__ == '__main__':
    main()

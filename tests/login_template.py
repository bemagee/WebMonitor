import os
import sys
import time
import json
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load credentials from the root .env file
load_dotenv()

def run_login_test():
    """
    REUSABLE LOGIN TEMPLATE WITH PERFORMANCE METRICS
    """
    
    # Configuration
    TARGET_URL = "https://example.com/login" 
    USER_SELECTOR = "input[name='username']"  
    PASS_SELECTOR = "input[name='password']"  
    SUBMIT_SELECTOR = "button[type='submit']" 
    SUCCESS_INDICATOR = ".dashboard"          
    
    metrics = {}
    username = os.getenv("TEST_USER")
    password = os.getenv("TEST_PASSWORD")

    if not username or not password:
        print("Error: TEST_USER or TEST_PASSWORD not found in .env file.")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 1. Measure Load Time
            start_load = time.time()
            page.goto(TARGET_URL)
            metrics["Load"] = time.time() - start_load
            
            # 2. Measure Login Action Time
            page.wait_for_selector(USER_SELECTOR)
            page.fill(USER_SELECTOR, username)
            page.fill(PASS_SELECTOR, password)
            
            start_action = time.time()
            page.click(SUBMIT_SELECTOR)
            page.wait_for_selector(SUCCESS_INDICATOR, timeout=10000)
            metrics["Action"] = time.time() - start_action
            
            # Print metrics for monitor.py to parse
            print(f"__METRICS__={json.dumps(metrics)}")
            
        except Exception as e:
            # Diagnostic Screenshot
            os.makedirs("screenshots", exist_ok=True)
            page.screenshot(path="screenshots/error_login.png")
            print(f"Login failed: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run_login_test()

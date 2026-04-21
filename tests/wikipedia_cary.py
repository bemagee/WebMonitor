import os
import time
import json
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load credentials
load_dotenv()

def test_wikipedia_cary():
    metrics = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # 1. Measure Navigation/Load Time
            start_load = time.time()
            page.goto("https://www.wikipedia.org")
            metrics["Load"] = time.time() - start_load
            
            # 2. Measure Search/Action Time
            start_action = time.time()
            page.fill("input[name='search']", "Cary, North Carolina")
            page.press("input[name='search']", "Enter")
            page.wait_for_selector("#firstHeading")
            metrics["Action"] = time.time() - start_action
            
            heading_text = page.inner_text("#firstHeading")
            assert "Cary, North Carolina" in heading_text
            
            # Print metrics for monitor.py to parse
            print(f"__METRICS__={json.dumps(metrics)}")
            
        except Exception as e:
            # Diagnostic Screenshot on Failure
            os.makedirs("screenshots", exist_ok=True)
            page.screenshot(path="screenshots/error_wikipedia_cary.png")
            print(f"Test failed: {e}")
            exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    test_wikipedia_cary()

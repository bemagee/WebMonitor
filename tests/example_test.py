import os
import time
import json
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

def run_test():
    metrics = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            start_load = time.time()
            page.goto("https://www.example.com")
            metrics["Load"] = time.time() - start_load
            
            start_action = time.time()
            h1_text = page.inner_text("h1")
            assert h1_text == "Example Domain"
            metrics["Action"] = time.time() - start_action
            
            print(f"__METRICS__={json.dumps(metrics)}")
            
        except Exception as e:
            os.makedirs("screenshots", exist_ok=True)
            page.screenshot(path="screenshots/error_example.png")
            print(f"Test failed: {e}")
            exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run_test()

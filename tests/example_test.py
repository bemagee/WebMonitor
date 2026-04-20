import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

def run_test():
    user = os.getenv("TEST_USER")
    password = os.getenv("TEST_PASSWORD")
    
    print(f"Running test for user: {user}...")

    with sync_playwright() as p:
        # Launch browser (headless by default)
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            # Navigate to example.com
            page.goto("https://www.example.com")
            
            # Simple check: Verify the <h1> tag contains "Example Domain"
            h1_text = page.inner_text("h1")
            assert h1_text == "Example Domain", f"Expected 'Example Domain', but got '{h1_text}'"
            
            print("Test passed: H1 matches!")
            
        except Exception as e:
            print(f"Test failed: {e}")
            exit(1) # Non-zero exit code indicates failure
        finally:
            browser.close()

if __name__ == "__main__":
    run_test()

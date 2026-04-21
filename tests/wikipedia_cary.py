import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load credentials (not needed for Wikipedia but good practice in this project)
load_dotenv()

def test_wikipedia_cary():
    print("Starting Wikipedia search test for 'Cary, North Carolina'...")

    with sync_playwright() as p:
        # Launch browser (headless=False if you want to see it happen)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # 1. Navigate to Wikipedia
            print("Navigating to Wikipedia...")
            page.goto("https://www.wikipedia.org")
            
            # 2. Type 'Cary, North Carolina' into the search bar
            # The search input ID is usually 'searchInput'
            page.fill("input[name='search']", "Cary, North Carolina")
            
            # 3. Press Enter to search
            page.press("input[name='search']", "Enter")
            
            # 4. Wait for the page to load and verify the heading
            # Wikipedia article headings are usually in an <h1> with ID 'firstHeading'
            page.wait_for_selector("#firstHeading")
            heading_text = page.inner_text("#firstHeading")
            
            print(f"Reached page with heading: {heading_text}")
            
            # Assertion to verify success
            assert "Cary, North Carolina" in heading_text, f"Expected heading to contain 'Cary, North Carolina', but got '{heading_text}'"
            
            print("Test passed: Successfully navigated to the Cary, NC Wikipedia page!")
            
        except Exception as e:
            print(f"Test failed: {e}")
            exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    test_wikipedia_cary()

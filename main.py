from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    with sync_playwright() as p:
        # Launch browser (you can use 'chromium', 'firefox', or 'webkit')
        browser = p.chromium.launch(headless=False)  # Set headless=True to run without GUI
        
        # Create a new browser context
        context = browser.new_context()
        
        # Create a new page
        page = context.new_page()
        
        # Navigate to the URL
        url = "https://www.crew-united.com/en/profil/login.asp"  # Replace with your target URL
        print(f"Navigating to: {url}")
        page.goto(url)
        
        # Wait for the page to load
        page.wait_for_load_state("networkidle")

        # Get credentials from environment variables
        username = os.getenv("CREW_UNITED_USERNAME")
        password = os.getenv("CREW_UNITED_PASSWORD")
        
        if not username or not password:
            print("Error: Please set CREW_UNITED_USERNAME and CREW_UNITED_PASSWORD in your .env file")
            browser.close()
            return

        username_input = page.query_selector("input[name='username']")
        username_input.fill(username)

        password_input = page.query_selector("input[name='password']")
        password_input.fill(password)

        login_button = page.query_selector("a.btn.js-cu-saveButton.waitable.icon-switch")
        login_button.click()

        
        # Print page title to confirm we're on the right page

        
        # Add your scraping logic here
        # For example:
        # content = page.content()
        # elements = page.query_selector_all("your-selector")
        
        # Close the browser
        browser.close()


if __name__ == "__main__":
    main()

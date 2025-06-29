from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        # Launch browser (you can use 'chromium', 'firefox', or 'webkit')
        browser = p.chromium.launch(headless=False)  # Set headless=True to run without GUI
        
        # Create a new browser context
        context = browser.new_context()
        
        # Create a new page
        page = context.new_page()
        
        # Navigate to the URL
        url = "https://example.com"  # Replace with your target URL
        print(f"Navigating to: {url}")
        page.goto(url)
        
        # Wait for the page to load
        page.wait_for_load_state("networkidle")
        
        # Print page title to confirm we're on the right page
        title = page.title()
        print(f"Page title: {title}")
        
        # Add your scraping logic here
        # For example:
        # content = page.content()
        # elements = page.query_selector_all("your-selector")
        
        # Close the browser
        browser.close()


if __name__ == "__main__":
    main()

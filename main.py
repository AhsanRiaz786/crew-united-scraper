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
        url = "https://www.crew-united.com/en/profil/login.asp"  # Replace with your target URL
        print(f"Navigating to: {url}")
        page.goto(url)
        
        # Wait for the page to load

 

        page.wait_for_load_state("networkidle")

        username_input = page.query_selector("input[name='username']")
        username_input.fill("test@test.com")

        password_input = page.query_selector("input[name='password']")
        password_input.fill("test1234")

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

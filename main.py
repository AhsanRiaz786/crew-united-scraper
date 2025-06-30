from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import time
import csv


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

        # Wait for login to complete by waiting for the logout button to appear.
        # This is more reliable than just waiting for network activity to stop.
        try:
            print("Waiting for login to complete...")
            page.wait_for_selector("a[href*='logout.asp']", timeout=15000)
            print("Login confirmed successfully.")
        except Exception:
            print("Login confirmation failed. Could not find logout button after 15 seconds.")
            print("The script may fail on the next page if the session is not active.")
        
        # Navigate to companies page after successful login
        target_url = "https://www.crew-united.com/en/companies/#!&filter=%5B%7B%22id%22%3A%22channel%22%2C%22value%22%3A%22company%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22searchTerm%22%2C%22value%22%3A%22%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22rootDepartment%22%2C%22value%22%3A%5B%22id%3A2%22%5D%2C%22settings%22%3A%22AND%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22department_collection%22%2C%22value%22%3A%5B%5D%2C%22settings%22%3A%22AND%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22country%22%2C%22value%22%3A%5B%22id%3A1%22%5D%2C%22settings%22%3A%22OR%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22city%22%2C%22value%22%3A%5B%5D%2C%22settings%22%3A%220km%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22numberOfResults%22%2C%22value%22%3A%22%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22pageSize%22%2C%22value%22%3A%2250%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22sortOrder%22%2C%22value%22%3A%22random_MvnAIIzlojArxj5kWNKZ%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22pagination%22%2C%22value%22%3A%221%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22displayStyle%22%2C%22value%22%3A%22card%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%5D&cardId=328300"
        page.goto(target_url)
        
        # Wait for the companies page to load
        page.wait_for_load_state("networkidle")
        print("Successfully navigated to companies page.")
        
        # Initialize counters and prepare CSV file
        page_number = 1
        total_items = 0
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"crew_united_companies_{timestamp}.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Define CSV header
            fieldnames = ['name', 'location1', 'location2', 'email', 'page']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)

            while True:
                print(f"\n=== SCRAPING PAGE {page_number} ===")
                
                # Give page time to load dynamic content
                time.sleep(2)
                page.wait_for_load_state("networkidle")
                
                # NOTE: These selectors were designed for freelancers and may need to be adjusted for company pages.
                items = page.query_selector_all("li.masonry-item")
                print(f"Found {len(items)} items on page {page_number}")

                if not items:
                    print("No items found. Selectors might be incorrect for the companies page.")
                
                for item in items:
                    try:
                        # Extract data using selectors (adjust if needed for companies)
                        name_element = item.query_selector("span.cu-ui-utility-member-name a, span.cu-ui-utility-company-name a")
                        item_name = name_element.inner_text().strip() if name_element else "N/A"
                        
                        location_element = item.query_selector("div.cu-ui-common-description.opt-secondary")
                        location1 = location_element.inner_text().strip() if location_element else "N/A"
                        location2 = "N/A" # Placeholder for additional location info
                        
                        email = "N/A"
                        email_element = item.query_selector("a[onclick*='putTogether']")
                        if email_element:
                            onclick_attr = email_element.get_attribute("onclick")
                            if onclick_attr and "putTogether" in onclick_attr:
                                start = onclick_attr.find("'") + 1
                                end = onclick_attr.find("'", start)
                                if start > 0 and end > start:
                                    obfuscated_email = onclick_attr[start:end]
                                    email = obfuscated_email.replace("$_isdot_$", ".").replace("$_isat_$", "@")
                        
                        # Write data row to CSV file
                        writer.writerow([item_name, location1, location2, email, page_number])
                        total_items += 1
                        
                        # Print progress to console
                        print(f"  {total_items}. Saved: {item_name}")
                        
                    except Exception as e:
                        print(f"Error extracting data for an item on page {page_number}: {str(e)}")
                        continue

                # Pagination: find and click the 'next' button
                next_button = page.query_selector("div.pagebuttons a.icon-chevron-right")
                
                if next_button:
                    print(f"Navigating to page {page_number + 1}...")
                    try:
                        next_button.click()
                        page_number += 1
                    except Exception as e:
                        print(f"Could not click next button: {str(e)}")
                        break
                else:
                    print("No more pages found. Scraping complete.")
                    break
        
        # Final summary
        print(f"\n=== SCRAPING SUMMARY ===")
        print(f"Total pages scraped: {page_number}")
        print(f"Total companies saved: {total_items}")
        print(f"Data saved to file: {filename}")
        
        # Close the browser
        browser.close()


if __name__ == "__main__":
    main()

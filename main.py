from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import time
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
        time.sleep(1)

        password_input = page.query_selector("input[name='password']")
        password_input.fill(password)
        time.sleep(1)

        login_button = page.query_selector("a.btn.js-cu-saveButton.waitable.icon-switch")
        time.sleep(1)
        login_button.click()

        # Wait for login to complete (wait for page to redirect or load)
        page.wait_for_load_state("networkidle")
        print("Login completed, navigating to freelancers page...")
        
        # Navigate to freelancers page after successful login
        freelancers_url = "https://www.crew-united.com/en/freelancers/#!&filter=%5B%7B%22id%22%3A%22channel%22%2C%22value%22%3A%22freelancer%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22searchTerm%22%2C%22value%22%3A%22%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22department_collection%22%2C%22value%22%3A%5B%22id%3A2%2F%2F129%2F%2F130%22%5D%2C%22settings%22%3A%22OR%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22country%22%2C%22value%22%3A%5B%22id%3A2%22%2C%22id%3A1%22%2C%22id%3A3%22%5D%2C%22settings%22%3A%22OR%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22city%22%2C%22value%22%3A%5B%5D%2C%22settings%22%3A%220km%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22language%22%2C%22value%22%3A%5B%5D%2C%22settings%22%3A%22AND%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22numberOfResults%22%2C%22value%22%3A%22%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22pageSize%22%2C%22value%22%3A%2250%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22sortOrder%22%2C%22value%22%3A%22random_kDf4CQq3WMtkvF1zz2YR%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22pagination%22%2C%22value%22%3A%221%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22displayStyle%22%2C%22value%22%3A%22card%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%5D"
        page.goto(freelancers_url)

        time.sleep(1)
        # Wait for the freelancers page to load
        page.wait_for_load_state("networkidle")

        # Initialize counters
        page_number = 1
        total_freelancers = 0
        all_freelancers_data = []

        while True:
            print(f"\n=== SCRAPING PAGE {page_number} ===")
            
            # Wait a bit for the page to fully load
            time.sleep(2)
            page.wait_for_load_state("networkidle")
            
            freelancers = page.query_selector_all("li.masonry-item")
            print(f"Found {len(freelancers)} freelancers on page {page_number}")

            for i, freelancer in enumerate(freelancers, 1):
                try:
                    # Extract name
                    name_element = freelancer.query_selector("span.cu-ui-utility-member-name.opt-state-premium a")
                    freelancer_name = name_element.inner_text().strip() if name_element else "N/A"
                    
                    # Extract location (primary location)
                    location_element = freelancer.query_selector("div.cu-ui-common-description.opt-secondary")
                    location1 = location_element.inner_text().strip() if location_element else "N/A"
                    
                    # Extract location2 (if there are multiple locations or address details)
                    # Looking for additional location info in contact details
                    contact_points = freelancer.query_selector_all("div.cu-ui-contact-point")
                    location2 = "N/A"
                    
                    # Extract email (handling obfuscated format)
                    email = "N/A"
                    email_element = freelancer.query_selector("div.cu-ui-contact-contact a[onclick*='putTogether']")
                    if email_element:
                        onclick_attr = email_element.get_attribute("onclick")
                        if onclick_attr and "putTogether" in onclick_attr:
                            # Extract the obfuscated email string
                            start = onclick_attr.find("'") + 1
                            end = onclick_attr.find("'", start)
                            if start > 0 and end > start:
                                obfuscated_email = onclick_attr[start:end]
                                # Decode the obfuscated email
                                email = obfuscated_email.replace("$_isdot_$", ".").replace("$_isat_$", "@")
                    
                    # Store freelancer data
                    freelancer_data = {
                        'name': freelancer_name,
                        'location1': location1,
                        'location2': location2,
                        'email': email,
                        'page': page_number
                    }
                    all_freelancers_data.append(freelancer_data)
                    total_freelancers += 1
                    
                    # Print the extracted information
                    print(f"  {total_freelancers}. {freelancer_name} | {location1} | {email}")
                    
                except Exception as e:
                    print(f"Error extracting data for freelancer {i} on page {page_number}: {str(e)}")
                    continue

            # Check if there's a next page button
            next_button = page.query_selector("div.cu-ui-button-group.opt-collapse.pagebuttons a.btn.icon.icon-chevron-right")
            
            if next_button:
                print(f"Navigating to page {page_number + 1}...")
                try:
                    # Click the next button
                    next_button.click()
                    page_number += 1
                    
                    # Wait for the next page to load
                    time.sleep(2)
                    page.wait_for_load_state("networkidle")
                except Exception as e:
                    print(f"Error navigating to next page: {str(e)}")
                    break
            else:
                print(f"No more pages found. Scraping completed!")
                break

        # Print summary
        print(f"\n=== SCRAPING SUMMARY ===")
        print(f"Total pages scraped: {page_number}")
        print(f"Total freelancers found: {total_freelancers}")
        
        # Optional: Save data to a file
        if all_freelancers_data:
            print(f"\nFirst 5 freelancers:")
            for i, freelancer in enumerate(all_freelancers_data[:5], 1):
                print(f"{i}. {freelancer['name']} | {freelancer['location1']} | {freelancer['email']}")

        
        # Print page title to confirm we're on the right page

        
        # Add your scraping logic here
        # For example:
        # content = page.content()
        # elements = page.query_selector_all("your-selector")
        
        # Close the browser
        browser.close()


if __name__ == "__main__":
    main()

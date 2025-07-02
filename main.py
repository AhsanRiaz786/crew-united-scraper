from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import time
import csv
import json


# Load environment variables from .env file
load_dotenv()


def load_cookies(context, cookie_file="cookies.json"):
    """Load cookies from file if it exists"""
    if os.path.exists(cookie_file):
        try:
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            print(f"Loaded {len(cookies)} cookies from {cookie_file}")
            return True
        except Exception as e:
            print(f"Error loading cookies: {e}")
            return False
    return False

def save_cookies(context, cookie_file="cookies.json"):
    """Save current cookies to file"""
    try:
        cookies = context.cookies()
        with open(cookie_file, 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"Saved {len(cookies)} cookies to {cookie_file}")
    except Exception as e:
        print(f"Error saving cookies: {e}")

def check_login_status(page):
    """Check if we're already logged in by looking for specific elements"""
    try:
        # Check for "My Profile" text (indicates we're logged in)
        profile_elements = page.query_selector_all('a')
        for element in profile_elements:
            text = element.inner_text().strip()
            if "My profile" in text or "My Profile" in text:
                print("✅ Already logged in - found 'My Profile' text")
                return True
        
        # Check for "Login" text (indicates we need to log in)
        for element in profile_elements:
            text = element.inner_text().strip()
            if text == "Login":
                print("❌ Not logged in - found 'Login' text")
                return False
        
        print("⚠️ Could not determine login status - neither 'Login' nor 'My Profile' text found")
        return False
    except Exception as e:
        print(f"Error checking login status: {e}")
        return False

def perform_login(page):
    """Perform the login process"""
    print("🔐 Starting login process...")
    
    # Get credentials from environment variables
    username = os.getenv("CREW_UNITED_USERNAME")
    password = os.getenv("CREW_UNITED_PASSWORD")
    
    if not username or not password:
        print("Error: Please set CREW_UNITED_USERNAME and CREW_UNITED_PASSWORD in your .env file")
        return False

    try:
        # Navigate to login page
        login_url = "https://www.crew-united.com/en/profil/login.asp"
        print(f"Navigating to login page: {login_url}")
        page.goto(login_url)
        page.wait_for_load_state("networkidle")

        # Fill in credentials
        username_input = page.query_selector("input[name='username']")
        username_input.fill(username)

        password_input = page.query_selector("input[name='password']")
        password_input.fill(password)

        # Click login button
        login_button = page.query_selector("a.btn.js-cu-saveButton.waitable.icon-switch")
        login_button.click()

        # Wait 3 seconds and then return
        print("Waiting 3 seconds after login attempt...")
        time.sleep(10)
        return True
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def main():
    with sync_playwright() as p:
        # Launch browser with additional options for headless mode
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        )
        
        # Create context with realistic browser settings
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        
        page = context.new_page()
        
        # Load existing cookies
        load_cookies(context)
        
        # Navigate to companies page first
        target_url = "https://www.crew-united.com/en/companies/#!&filter=%5B%7B%22id%22%3A%22channel%22%2C%22value%22%3A%22company%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22searchTerm%22%2C%22value%22%3A%22%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22rootDepartment%22%2C%22value%22%3A%5B%22id%3A2%22%5D%2C%22settings%22%3A%22AND%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22department_collection%22%2C%22value%22%3A%5B%5D%2C%22settings%22%3A%22AND%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22country%22%2C%22value%22%3A%5B%22id%3A1%22%5D%2C%22settings%22%3A%22OR%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22city%22%2C%22value%22%3A%5B%5D%2C%22settings%22%3A%220km%22%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22numberOfResults%22%2C%22value%22%3A%22%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22pageSize%22%2C%22value%22%3A%2250%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22sortOrder%22%2C%22value%22%3A%22random_MvnAIIzlojArxj5kWNKZ%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22pagination%22%2C%22value%22%3A%221%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%2C%7B%22id%22%3A%22displayStyle%22%2C%22value%22%3A%22card%22%2C%22settings%22%3A%5B%5D%2C%22isReadOnly%22%3Afalse%7D%5D"
        
        # Detect what we're scraping based on URL
        if "/companies/" in target_url:
            scraping_type = "companies"
            item_type = "company"
        elif "/freelancers/" in target_url:
            scraping_type = "freelancers"
            item_type = "freelancer"
        else:
            scraping_type = "unknown"
            item_type = "item"
        
        print(f"🎯 Navigating to {scraping_type} page...")
        try:
            page.goto(target_url, timeout=30000)  # 30 second timeout
            page.wait_for_load_state("networkidle", timeout=15000)  # 15 second timeout
        except Exception as e:
            print(f"⚠️ Error loading initial page: {e}")
            print("Trying to continue anyway...")
        
        # Check if we're logged in on the target page
        max_login_attempts = 3
        login_attempts = 0
        
        while login_attempts < max_login_attempts:
            if check_login_status(page):
                print(f"✅ Login confirmed! Starting {scraping_type} scraping...")
                save_cookies(context)  # Save cookies after confirmed login
                break
            else:
                login_attempts += 1
                print(f"❌ Not logged in. Attempt {login_attempts}/{max_login_attempts}")
                
                if login_attempts >= max_login_attempts:
                    print("❌ Failed to login after maximum attempts. Exiting...")
                    browser.close()
                    return
                
                # Perform login
                if not perform_login(page):
                    print("❌ Login process failed. Exiting...")
                    browser.close()
                    return
                
                # Navigate back to target page to check login status
                print(f"🎯 Navigating back to {scraping_type} page...")
                try:
                    page.goto(target_url, timeout=30000)
                    page.wait_for_load_state("networkidle", timeout=15000)
                except Exception as e:
                    print(f"⚠️ Error loading page after login: {e}")
                    print("Trying to continue anyway...")
        
        # Initialize counters and prepare CSV file
        page_number = 1
        total_items = 0
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"crew_united_{scraping_type}_{timestamp}.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Define CSV header (removed page column)
            fieldnames = ['name', 'location1', 'location2', 'email']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            csvfile.flush()  # Ensure header is written immediately

            while True:
                print(f"\n=== SCRAPING {scraping_type.upper()} PAGE {page_number} ===")
                
                # Give page time to load dynamic content with error handling
                try:
                    time.sleep(2)
                    page.wait_for_load_state("networkidle", timeout=15000)
                    
                    # Additional wait for headless mode - wait for masonry items to be visible
                    try:
                        page.wait_for_selector("li.masonry-item", timeout=10000)
                        print("✅ Page content loaded successfully")
                    except:
                        print("⚠️ Masonry items not found, but continuing...")
                        
                except Exception as e:
                    print(f"⚠️ Page loading timeout on page {page_number}: {e}")
                    print("Continuing with current page state...")
                
                try:
                    # Additional wait to ensure JavaScript has finished rendering
                    time.sleep(2)
                    
                    items = page.query_selector_all("li.masonry-item")
                    print(f"Found {len(items)} {item_type}s on page {page_number}")

                    if not items:
                        print(f"No {item_type}s found. Selectors might be incorrect for the {scraping_type} page.")
                        print("Trying to continue to next page...")
                    
                    for item in items:
                        try:
                            # Additional wait to ensure item is fully loaded
                            time.sleep(0.1)
                            
                            # Extract data using selectors (works for both companies and freelancers)
                            name_element = item.query_selector("span.cu-ui-utility-member-name a, span.cu-ui-utility-company-name a")
                            item_name = name_element.inner_text().strip() if name_element else "N/A"
                            
                            location_element = item.query_selector("div.cu-ui-common-description.opt-secondary")
                            location_text = location_element.inner_text().strip() if location_element else ""
                            
                            # Split locations by comma
                            if location_text:
                                locations = [loc.strip() for loc in location_text.split(',')]
                                location1 = locations[0] if len(locations) > 0 else "N/A"
                                location2 = locations[1] if len(locations) > 1 else "N/A"
                            else:
                                location1 = "N/A"
                                location2 = "N/A"
                            
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
                            
                            # Write data row to CSV file (removed page column)
                            writer.writerow([item_name, location1, location2, email])
                            csvfile.flush()  # Immediately save to disk
                            total_items += 1
                            
                            # Print progress to console
                            print(f"  {total_items}. Saved: {item_name}")
                            
                        except Exception as e:
                            print(f"⚠️ Error extracting data for a {item_type}: {str(e)}")
                            print("Continuing with next item...")
                            continue

                except Exception as e:
                    print(f"⚠️ Error processing page {page_number}: {str(e)}")
                    print("Trying to continue to next page...")

                # Pagination: find and click the 'next' button with better logic
                try:
                    next_button = page.query_selector("div.pagebuttons a.icon-chevron-right")
                    
                    # Check if we're on the last page by looking at pagination structure
                    active_page_element = page.query_selector("div.pages a.opt-active")
                    active_page_number = None
                    if active_page_element:
                        active_page_text = active_page_element.inner_text().strip()
                        try:
                            active_page_number = int(active_page_text)
                        except:
                            pass
                    
                    # Get all page numbers to find the maximum
                    page_links = page.query_selector_all("div.pages a")
                    max_page_number = 0
                    for link in page_links:
                        try:
                            page_num = int(link.inner_text().strip())
                            max_page_number = max(max_page_number, page_num)
                        except:
                            continue
                    
                    print(f"Current page: {active_page_number}, Max page: {max_page_number}")
                    
                    # Check if we can continue to next page
                    should_continue = False
                    if next_button and active_page_number and max_page_number:
                        if active_page_number < max_page_number:
                            should_continue = True
                            print(f"Next page available. Moving from page {active_page_number} to {active_page_number + 1}")
                        else:
                            print(f"Reached last page ({active_page_number}/{max_page_number}). Stopping pagination.")
                    elif next_button:
                        # Fallback: if we can't determine page numbers but next button exists
                        print("Could not determine page numbers, but next button exists. Trying to continue...")
                        should_continue = True
                    
                    if should_continue and next_button:
                        try:
                            # Store current page number before clicking
                            old_page_number = active_page_number
                            
                            next_button.click()
                            page_number += 1
                            
                            # Wait and check if we actually moved to a new page
                            time.sleep(3)  # Wait 3 seconds between page movements
                            try:
                                page.wait_for_load_state("networkidle", timeout=15000)
                            except Exception as e:
                                print(f"⚠️ Timeout waiting for page {page_number} to load: {e}")
                                print("Continuing anyway...")
                            
                            # Verify we moved to a new page
                            try:
                                new_active_page_element = page.query_selector("div.pages a.opt-active")
                                new_page_number = None
                                if new_active_page_element:
                                    new_page_text = new_active_page_element.inner_text().strip()
                                    try:
                                        new_page_number = int(new_page_text)
                                    except:
                                        pass
                                
                                if old_page_number and new_page_number:
                                    if new_page_number <= old_page_number:
                                        print(f"⚠️ Page didn't advance properly (went from {old_page_number} to {new_page_number}). Stopping.")
                                        break
                                    else:
                                        print(f"✅ Successfully moved to page {new_page_number}")
                            except Exception as e:
                                print(f"⚠️ Could not verify page transition: {e}")
                                print("Continuing anyway...")
                            
                        except Exception as e:
                            print(f"⚠️ Could not click next button: {str(e)}")
                            print("Attempting to continue...")
                            # Try to continue anyway in case the page loaded
                            page_number += 1
                            if page_number > 10:  # Prevent infinite loops
                                print("⚠️ Too many navigation errors. Stopping.")
                                break
                    else:
                        print("No more pages found or reached last page. Scraping complete.")
                        break
                    
                except Exception as e:
                    print(f"⚠️ Error during pagination on page {page_number}: {str(e)}")
                    print("Attempting to continue...")
                    page_number += 1
                    if page_number > 10:  # Prevent getting stuck
                        print("⚠️ Too many pagination errors. Stopping.")
                        break
                
                # Safety check: prevent infinite loops
                if page_number > 50:  # Reasonable upper limit
                    print("⚠️ Safety limit reached (50 pages). Stopping to prevent infinite loop.")
                    break
        
        # Final summary
        print(f"\n=== {scraping_type.upper()} SCRAPING SUMMARY ===")
        print(f"Total pages processed: {page_number}")
        print(f"Total {item_type}s saved: {total_items}")
        print(f"Data saved to file: {filename}")
        print(f"✅ All data has been continuously saved during scraping")
        
        # Close the browser
        browser.close()


if __name__ == "__main__":
    main()

import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def click_page(driver, wait, page_no):
    max_attempts = 10
    for _ in range(max_attempts):
        try:
            page_btn = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f'button[aria-label="Page {page_no}"]')))
            driver.execute_script("arguments[0].scrollIntoView();", page_btn)
            time.sleep(1)
            page_btn.click()
            print(f"📄 Clicked Page {page_no}")
            time.sleep(4)
            return True
        except:
            try:
                ellipsis_buttons = driver.find_elements(By.CSS_SELECTOR, 'button > span')
                for el in ellipsis_buttons:
                    if el.text.strip() == '…':
                        driver.execute_script("arguments[0].scrollIntoView();", el)
                        el.click()
                        print("➡️ Clicked '...' to reveal more pages")
                        time.sleep(3)
                        break
            except Exception as e:
                print(f"⚠️ Couldn't click ellipsis: {e}")
    print(f"❌ Failed to click Page {page_no} after multiple attempts")
    return False


def scrape_jobs(username, password, job_title, location, page_range_str):
    start_page, end_page = map(int, page_range_str.split("-"))

    # Setup Chrome
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    # Login
    driver.get("https://www.linkedin.com/login")
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password, Keys.RETURN)
    print("✅ Logged in")
    time.sleep(3)

    # Job search
    driver.get("https://www.linkedin.com/jobs")
    location_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'input[aria-label*="City, state, or zip code"]')))
    location_input.clear()
    location_input.send_keys(location)
    time.sleep(1)
    location_input.send_keys(Keys.RETURN)

    job_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'input[aria-label*="Search by title"]')))
    job_input.clear()
    job_input.send_keys(job_title, Keys.RETURN)
    print(f"🔍 Searching '{job_title}' jobs in '{location}'")
    time.sleep(5)

    # Detect available pages
    page_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label^="Page "] span')
    available_pages = [int(btn.text.strip()) for btn in page_buttons if btn.text.strip().isdigit()]
    max_available = max(available_pages) if available_pages else 1
    print(f"📃 Max available pages: {max_available}")

    valid_pages = [p for p in range(start_page, end_page + 1) if p <= max_available]

    if not valid_pages:
        print(f"⚠️ No pages available in range {start_page}-{end_page}. Exiting.")
        return

    job_data = []
    collected_job_ids = set()

    for current_page in valid_pages:
        if current_page > 1:
            clicked = click_page(driver, wait, current_page)
            if not clicked:
                continue

        print(f"📄 Scraping Page {current_page}...")

        scrollable_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
            "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > div"
        )))

        for _ in range(10):
            driver.execute_script("arguments[0].scrollBy(0, 300);", scrollable_div)
            time.sleep(0.5)

        job_cards = driver.find_elements(By.CSS_SELECTOR, "li.scaffold-layout__list-item")
        print(f"📌 Found {len(job_cards)} jobs")

        for card in job_cards:
            try:
                job_id = card.get_attribute("data-occludable-job-id")
                if job_id and job_id not in collected_job_ids:
                    title_elem = card.find_element(By.CSS_SELECTOR, "a.job-card-container__link")
                    company_elem = card.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__subtitle span")
                    location_elem = card.find_element(By.CSS_SELECTOR, "ul.job-card-container__metadata-wrapper li span")

                    job_data.append({
                        "Title": title_elem.text.strip(),
                        "Company": company_elem.text.strip(),
                        "Location": location_elem.text.strip(),
                        "Link": title_elem.get_attribute("href")
                    })
                    collected_job_ids.add(job_id)
                    print(f"✅ {title_elem.text.strip()} at {company_elem.text.strip()}")
            except Exception as e:
                print(f"⚠️ Skipped a job due to error: {e}")

    # Save to Downloads folder as Excel
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    safe_title = job_title.replace(" ", "_")
    filename = f"{safe_title}_{timestamp}.xlsx"
    output_path = os.path.join(downloads_folder, filename)

    df = pd.DataFrame(job_data)
    df.to_excel(output_path, index=False)

    print(f"📁 Saved {len(job_data)} jobs to {output_path}")

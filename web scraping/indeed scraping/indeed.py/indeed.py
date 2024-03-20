from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

url = "https://fr.indeed.com/"
driver.get(url)

wait = WebDriverWait(driver, 10)

# Function to extract job details
def extract_job_details(link):
    try:
        driver.get(link)
        offer_link = driver.find_element(By.CSS_SELECTOR, "a.jobtitle.turnstileLink").get_attribute("href")
        position = driver.find_element(By.CSS_SELECTOR, "h3.jobsearch-JobInfoHeader-title").text
        company = driver.find_element(By.CSS_SELECTOR, "div.icl-u-lg-mr--sm").text
        release = re.search(r"(\d+)\s+días", driver.find_element(By.CSS_SELECTOR, "div.jobsearch-JobMetadataFooter").text)
        release_day = release.group(1) if release else "Unknown"
        condition = "Python" if "Python" in driver.page_source else "None"
        return offer_link, position, company, release_day, condition
    except Exception as e:
        print(f"Failed to extract details for {link}: {e}")
        return None, None, None, None, None

# Perform job search
keyword = "data madrid"
print("Looking for:", keyword)
search_bar = driver.find_element(By.NAME, "q")
search_bar.clear()
search_bar.send_keys(keyword)
search_bar.send_keys(Keys.RETURN)

# Scraping job links
links = []
max_pages = 5  # Set maximum number of pages to scrape
page_count = 0
while True:
    try:
        new_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".jobtitle.turnstileLink")))
        links.extend([l.get_attribute("href") for l in new_links])
        next_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Suivant']")))
        next_page.click()
        page_count += 1
        if page_count >= max_pages:
            print(f"Scraped {max_pages} pages. Exiting loop.")
            break
    except:
        print("Links scraped")
        break

# Extract job details
data = []
for link in links:
    data.append(extract_job_details(link))

# Saving data to CSV
output_filename = keyword.replace(" ", "-") + ".csv"
with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["indeed_link", "offer_link", "position", "company", "release day", "contains"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i, (link, offer_link, position, company, release_day, condition) in enumerate(data, start=1):
        writer.writerow({"indeed_link": link, "offer_link": offer_link, "position": position, "company": company, "release day": release_day, "contains": condition})

print(f"{output_filename} file available")

driver.quit()

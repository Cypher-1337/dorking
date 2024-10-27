from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_google(query, max_results=150):
    # Set up Selenium with Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # Optional, may help on some servers
    options.add_argument("--disable-software-rasterizer")  # Optional
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL and search query
    url = f"https://www.google.com/search?q={query}&filter=0&tbs=qdr:d"
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    results = []
    seen_links = set()  # Set to track unique links

    while len(results) < max_results:
        # Find all result links on the current page
        links = driver.find_elements(By.CSS_SELECTOR, "a[href]")

        for link in links:
            title = link.text
            href = link.get_attribute("href")
            # Filter out Google internal links and duplicates
            if href and "google.com" not in href and href not in seen_links :
                result = {"title": title, "link": href}
                results.append(result)
                seen_links.add(href)  # Track seen links

        # Check if we've collected enough results
        if len(results) >= max_results:
            break

        # Click the "More results" button to load more results (Google doesn't have a button, we use pagination)
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '#pnnext')
            next_button.click()
            time.sleep(2)  # Wait for new results to load
        except:
            break

    # Close the browser
    driver.quit()
    return results[:max_results]

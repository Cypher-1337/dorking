from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def read_domains(file_path):
    """Read a list of domains from a file."""
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]  # Remove empty lines
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
    

def search_duckduckgo(query, max_results=150):
    # Set up Selenium with Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # Optional, may help on some servers
    options.add_argument("--disable-software-rasterizer")  # Optional
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL and search query
    url = f"https://duckduckgo.com/?q={query}&df=d"
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    results = []
    seen_links = set()  # Set to track unique links

    while len(results) < max_results:
        # Find all result links on the current page
        links = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='result-title-a']")
        # print(f"Found {len(links)} links on this page.")  # Debugging output

        for link in links:
            title = link.text
            href = link.get_attribute("href")
            # Filter out DuckDuckGo internal links
            if href and "duckduckgo.com" not in href and href not in seen_links :
                result = {"title": title, "link": href}
                results.append(result)
                seen_links.add(href)  # Track seen links
        
        
        # Check if we've collected enough results
        if len(results) >= max_results:
            break

        # Click the "More results" button to load more results
        try:
            more_button = driver.find_element(By.ID, "more-results")
            more_button.click()
            time.sleep(2)  # Wait for new results to load
        except:
            break

    # Close the browser
    driver.quit()
    return results[:max_results]

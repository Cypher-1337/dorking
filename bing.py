from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def search_bing(query, max_results=150, results_per_page=10):
    # Set up Selenium with Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # Optional, may help on some servers
    options.add_argument("--disable-software-rasterizer")  # Optional
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    results = []
    seen_links = set()  # Track unique links for this run
    page_number = 1

    while len(results) < max_results:
        # Calculate the starting result index for each page (1, 11, 21, etc.)
        start_index = (page_number - 1) * results_per_page + 1
        url = f'https://www.bing.com/search?q={query}&first={start_index}&FORM=PERE{page_number}&filters=ex1%3a"ez1"'
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        # Find all result links on the current page with a specific CSS class
        links = driver.find_elements(By.CSS_SELECTOR, "li.b_algo h2 a")

        # Track if any new links were added

        for link in links:
            title = link.text
            href = link.get_attribute("href")
            # Filter out duplicates
            if href and href not in seen_links:
                results.append({"title": title, "link": href})
                seen_links.add(href)  # Track seen links

            # Stop if we've reached the max results
            if len(results) >= max_results:
                break

        # Check if we've reached the max results
        if len(results) >= max_results:
            break

        # Check if there are more pages and move to the next page
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, ".sb_pagN")  # CSS selector for Bing's 'Next' button
            next_button.click()
            time.sleep(2)  # Wait for new results to load
            page_number += 1
        except:
            break

    driver.quit()
    return results[:max_results]

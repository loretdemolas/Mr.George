# search.py
import sqlite3
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


# Finds all jobs with the query
def search_jobs(driver, query, job_queue):
    # Perform the Google search
    driver.get(f"https://www.google.com/search?q={query}")

    # Scroll to the bottom of the page to load more results
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolling...")

        # Wait for the new results to load
        time.sleep(2)  # Adjust the sleep time as needed

        # Retrieve the job URLs from search results
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        for result in search_results:
            try:
                link_element = result.find_element(By.CSS_SELECTOR, "a")
                url = link_element.get_attribute("href")
                if "boards.greenhouse.io" in url:
                    connection = sqlite3.connect('logged_urls.db')
                    cursor = connection.cursor()
                    cursor.execute("SELECT url FROM logged_urls WHERE url = ?", (url,))
                    if cursor.fetchone() is None:
                        job_queue.put(url)
                        print("New Results added:", url)
                        connection.close()
            except StaleElementReferenceException:
                continue

        # Check if we have reached the bottom of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
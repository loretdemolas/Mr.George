#filter.py

import sqlite3
from selenium.webdriver.common.by import By

def filter_jobs(driver, logged_queue, site, job, location):
    connection_filtered = sqlite3.connect('filtered_urls.db')
    cursor_filtered = connection_filtered.cursor()
    print("Filtering Jobs...")

    while True:
        url = logged_queue.get()
        if url is None:
            print("job finshed")
            break

        # Load the job application page
        driver.get(url)

        # Check if the page has an apply button
        iframe_elements = driver.find_elements(By.TAG_NAME, "iframe")
        if len(iframe_elements) > 0:
        # If iframe elements are found, proceed with switching to the first one
            first_iframe = iframe_elements[0]
            driver.switch_to.frame(first_iframe)

        apply_button = driver.find_elements(By.ID, "apply_button")
        if len(apply_button) > 0:
            status = "approved"
            print("Approved(1/2):", url)
            if location != "Remote":
                # Check if the site, job, and location match the URL
                location_elements = driver.find_elements(By.CSS_SELECTOR, "div.location")
                location_texts = [element.text for element in location_elements]
                if location in location_texts:
                    status = "approved"
                    print("Approved(2/2):", url)
                else:
                    status = "denied"
                    print("Denied, wrong location:", url)
            else:
                status = "approved"
                print("Approved(2/2):", url)
        else:
            status = "denied"
            print("Denied, no apply button on page:" , url)    

        # Store the URL in the filtered_urls.db database
        cursor_filtered.execute("INSERT INTO filtered_urls (url, status) VALUES (?, ?)", (url, status))
        connection_filtered.commit()
        print("Ready to apply")

    connection_filtered.close()

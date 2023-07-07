import traceback
import time
from threading import Thread
from queue import Queue
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3

# Creates databases
def create_databases():
    # Creating logged_urls database
    connection_logged = sqlite3.connect('logged_urls.db')
    cursor_logged = connection_logged.cursor()
    cursor_logged.execute('''CREATE TABLE IF NOT EXISTS logged_urls
                            (url TEXT PRIMARY KEY, search_term TEXT)''')
    connection_logged.commit()
    connection_logged.close()

    # Creating filtered_urls database
    connection_filtered = sqlite3.connect('filtered_urls.db')
    cursor_filtered = connection_filtered.cursor()
    cursor_filtered.execute('''CREATE TABLE IF NOT EXISTS filtered_urls
                              (url TEXT PRIMARY KEY, status TEXT)''')
    connection_filtered.commit()
    connection_filtered.close()


# Finds all jobs with the query
def search_jobs(driver, query, job_queue, logged_urls):
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

        # Check if we have reached the bottom of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Records URL to persist results to subsequent searches
def log_jobs(job_queue, logged_urls, query):
    connection = sqlite3.connect('logged_urls.db')
    cursor = connection.cursor()

    while True:
        job_url = job_queue.get()
        if job_url is None:
            break

        # Write job details to the SQLite database
        cursor.execute("INSERT INTO logged_urls (url, search_term) VALUES (?, ?)", (job_url, query))
        connection.commit()

        # Add the URL to the logged URLs set
        logged_urls.add(job_url)

    connection.close()

def main():
    try:
        create_databases()

        # Set up the web driver
        driver = webdriver.Chrome()  # Adjust based on your browser and driver choice
        driver.implicitly_wait(10)  # Add an implicit wait to handle page loading

        # Input for Google query
        site = "greenhouse.io"
        job = "Event Planner"
        location = "Orlando"
        time_filter = "last 7 days"
        query = 'site:' + site + ' "' + job + '" "' + location + '" ' + time_filter
        print(query)

        # Create a queue to store job URLs
        job_queue = Queue()

        # Create a set to store logged URLs
        logged_urls = set()

        # Create and start the search thread
        search_thread = Thread(target=search_jobs, args=(driver, query, job_queue, logged_urls))
        search_thread.start()

        # Create and start the log thread
        log_thread = Thread(target=log_jobs, args=(job_queue, logged_urls, query))
        log_thread.start()

        # Wait for the search thread to finish
        search_thread.join()

        # Wait for the log thread to finish
        job_queue.put(None)
        log_thread.join()

        print("Job details saved to 'job_list.txt'")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()

    finally:
        # Close the web driver
        driver.quit()

if __name__ == "__main__":
    main()



    # Iterate over job URLs
  
    # Load the job application page
        
    # Preview the job details
                
    # Prompt user for action
               
    # Upload resume (assuming input field has id 'resume')
          
    # Fill in additional fields if necessary
                        
    # Submit the application
                        
    # Wait for submission success message (assuming it has class 'success-message')
    

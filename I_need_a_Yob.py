import traceback
import time
from threading import Thread
from queue import Queue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
            if "boards.greenhouse.io" in url and url not in logged_urls:
                job_queue.put(url)
                print("New Results added:", url)

        # Check if we have reached the bottom of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def log_jobs(driver, job_queue, logged_urls):
    # Open a text file to save the job details
    with open("job_list.txt", "a", encoding="utf-8") as file:
        while not job_queue.empty():
            job_url = job_queue.get()
            # Load the job application page
            driver.get(job_url)
            #Check to see if apply button exists

            # Preview the job details
            job_title = driver.find_element(By.CSS_SELECTOR, "h1.app-title").text
            company_name = driver.find_element(By.CSS_SELECTOR, "span.company-name").text
            job_location = driver.find_element(By.CSS_SELECTOR, "div.location").text

            # Print job details
            print(f"Job Title: {job_title}")
            print(f"Company: {company_name}")
            print(f"Location: {job_location}")
            print("----------------------")

            # Write job details to the text file
            file.write(f"Job Title: {job_title}\n")
            file.write(f"Company: {company_name}\n")
            file.write(f"Location: {job_location}\n")
            file.write("----------------------\n")

            # Add the URL to the logged URLs
            logged_urls.add(job_url)

def main():
    try:
        # Set up the web driver
        driver = webdriver.Chrome()  # Adjust based on your browser and driver choice
        driver.implicitly_wait(10)  # Add an implicit wait to handle page loading

        # User input for Google query
        query = input("Enter your Google query: ") # site:greenhouse.io "remote"

        # Create a queue to store job URLs
        job_queue = Queue()

        # Create a set to store logged URLs
        logged_urls = set()

        # Create and start the search thread
        search_thread = Thread(target=search_jobs, args=(driver, query, job_queue, logged_urls))
        search_thread.start()

        # Create and start the log thread
        log_thread = Thread(target=log_jobs, args=(driver, job_queue, logged_urls))
        log_thread.start()

        # Wait for the search thread to finish
        search_thread.join()

        # Wait for the log thread to finish
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
    

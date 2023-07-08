import traceback
from threading import Thread
from queue import Queue
from selenium import webdriver
from database import create_databases
from search import search_jobs
from log_utils import log_jobs
from filter import filter_jobs
from datetime import date, timedelta
import report

def main():
    try:
        create_databases()

        # Set up the web driver
        driver = webdriver.Chrome()  # Adjust based on your browser and driver choice
        driver.implicitly_wait(10)  # Add an implicit wait to handle page loading

        # Input for Google query
        # Calculate the date range
        end_date = date.today()
        start_date = end_date - timedelta(days=7)

        # Format the dates in YYYY-MM-DD format
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        site = "greenhouse.io"
        job = "Software Developer"
        location = "orlando"
        query = 'site:' + site + ' "' + job + '" "' + location + '" daterange:' + start_date_str + '..' + end_date_str
        print(query)


        # Queue Creation 
        job_queue = Queue()
        logged_queue = Queue()

        # Creating and starting threads
        search_thread = Thread(target=search_jobs, args=(driver, query, job_queue))
        search_thread.start()

        log_thread = Thread(target=log_jobs, args=(job_queue, logged_queue, query))
        log_thread.start()

     

        #Threads are finishing and queues are being capped
        search_thread.join()
        job_queue.put(None)
        log_thread.join()

        #Phase two: filter
        filter_thread = Thread(target=filter_jobs, args=(driver, logged_queue, site, job, location))
        filter_thread.start()

        logged_queue.put(None)
        filter_thread.join()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()

    finally:
        # Close the web driver
        driver.quit()
        # Print the report
        report.print_filtered_urls()
        report.print_logged_urls()

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
    

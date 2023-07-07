# Records URL to persist results to subsequent searches
import sqlite3


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
# database.py
import sqlite3

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

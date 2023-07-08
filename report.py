import sqlite3

def print_filtered_urls():
    print("Filtered URLs:")
    connection_filtered = sqlite3.connect('filtered_urls.db')
    cursor_filtered = connection_filtered.cursor()
    cursor_filtered.execute("SELECT * FROM filtered_urls")
    rows_filtered = cursor_filtered.fetchall()
    for row in rows_filtered:
        print(row)
    connection_filtered.close()

def print_logged_urls():
    print("Logged URLs:")
    connection_logged = sqlite3.connect('logged_urls.db')
    cursor_logged = connection_logged.cursor()
    cursor_logged.execute("SELECT * FROM logged_urls")
    rows_logged = cursor_logged.fetchall()
    for row in rows_logged:
        print(row)
    connection_logged.close()

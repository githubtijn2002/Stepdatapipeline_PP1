import sqlite3
import os

def insert_data(data):
    # Define the path to the SQLite database
    db_path = '/app/db/steps.db'
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS steps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE,
                    steps INTEGER)''')
    c.execute("INSERT OR IGNORE INTO steps (date, steps) VALUES (?, ?)",
              (data['minute_str'], data['steps']))
    conn.commit()
    conn.close()

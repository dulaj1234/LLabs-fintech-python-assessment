import sqlite3
import os

# DB file creation path
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "market_data.db")

def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
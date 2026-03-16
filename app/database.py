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

def init_db():
    """
    Creates the table if it doesn't already exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monthly_stock_prices (
            symbol  TEXT NOT NULL,
            date    TEXT NOT NULL,
            high    TEXT NOT NULL,
            low     TEXT NOT NULL,
            volume  INTEGER NOT NULL,
            PRIMARY KEY (symbol, date)
        )
    """)

    conn.commit()
    conn.close()

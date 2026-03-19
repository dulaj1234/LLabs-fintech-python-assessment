import sqlite3
import os
import datetime

# DB file creation path
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "market_data.db")

def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
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

def insert_monthly_mkt_data(symbol: str, monthly_data: dict):
    """
    Inserts all monthly market data rows for a symbol into the DB
    """
    conn = get_connection()
    cursor = conn.cursor()

    current_year = str(datetime.date.today().year)

    for date, values in monthly_data.items():

        if date.startswith(current_year):
            # Current year — UPSERT
            # Update if exists, insert if not
            cursor.execute("""
                INSERT INTO monthly_stock_prices
                    (symbol, date, high, low, volume)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(symbol, date)
                DO UPDATE SET
                    high   = excluded.high,
                    low    = excluded.low,
                    volume = excluded.volume
            """,
            (
                symbol.upper(),
                date,
                values["2. high"],
                values["3. low"],
                values["5. volume"]
            ))

        else:
            # Past year — INSERT OR IGNORE
            # Never overwrite historical data
            cursor.execute("""
                INSERT OR IGNORE INTO monthly_stock_prices
                    (symbol, date, high, low, volume)
                VALUES (?, ?, ?, ?, ?)
            """,
            (
                symbol.upper(),
                date,
                values["2. high"],
                values["3. low"],
                values["5. volume"]
            ))

    conn.commit()
    conn.close()

def get_annual_mkt_data(symbol: str, year: str):
    """
    Returns the array of annual data for a given symbol and year in [high, low, volumn] format
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT high, low, volume FROM monthly_stock_prices WHERE symbol = ? AND date like ?
    """,
    (
        symbol.upper(),
        f"{year}-%"
    ))

    rows = cursor.fetchall()
    conn.close()
    
    return [max(float(row["high"]) for row in rows), 
            min(float(row["low"]) for row in rows),
            sum(int(row["volume"]) for row in rows)]

def is_data_available(symbol: str, year: str) -> bool:
    """
    This returns True or False by checking whether there are already data for the given symbol and year in DB 
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) as count FROM monthly_stock_prices WHERE symbol = ? AND date LIKE ?
    """,
    (
        symbol.upper(),
        f"{year}-%"
    ))

    row = cursor.fetchone()
    conn.close()

    return row["count"] > 0
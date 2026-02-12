import sqlite3
from pathlib import Path

DB_PATH = Path("urls.db")


def get_connection():
    """
    Createsand returns a connection to the database
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes the database by creating the necessary tables
    """
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shorten_url TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            )
        """)
        conn.commit()
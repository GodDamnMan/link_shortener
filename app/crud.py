import sqlite3

from .database import get_connection

def get_original_url(shorten_url:str) -> str | None:
    """
    Method that searches the original url in database
    Can return original url if found, or None if shorten_url
    is not presented in database
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT original_url FROM urls WHERE shorten_url = ?", (shorten_url,)
        ).fetchone()
            
        if row:
            return row["original_url"]

        return None
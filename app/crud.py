import sqlite3

from .database import get_connection
from .utils import generate_short_code


def get_original_url(custom_code:str) -> str | None:
    """
    Method that searches the original url in database
    Can return original url if found, or None if custom_code
    is not presented in database
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT original_url FROM urls WHERE custom_code = ?", (custom_code,)
        ).fetchone()
            
        if row:
            return row["original_url"]

        return None
    


def create_shorten_url(original_url: str, custom_code: str | None = None) -> str:
    """
    function that crates a short url, pushes it into database
    """
    conn = get_connection()
    try:
        if custom_code:
            try:
                conn.execute(
                    "INSERT INTO urls (custom_code, original_url) VALUES (?, ?)",
                    (custom_code, original_url),
                )

                conn.commit()
                
                return custom_code
            except sqlite3.IntegrityError:
                # TODO log and response if collison
                return None


        # TODO make better generating code in order to avoid collisions
        for _ in range(100):
            custom_code = generate_short_code()
            try:
                conn.execute(
                    "INSERT INTO urls (custom_code, original_url) VALUES (?, ?)",
                    (custom_code, original_url),
                )
                conn.commit()
                return custom_code
            except sqlite3.IntegrityError:
                continue
        
        raise RuntimeError("Не удалось сгенерировать уникальный код")
    finally:
        conn.close()
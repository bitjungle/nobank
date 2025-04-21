import sqlite3
from pathlib import Path
import os
from typing import Optional

def get_db_connection() -> sqlite3.Connection:
    """
    Connect to the SQLite database at the known location.
    Returns a connection with row_factory set to sqlite3.Row.
    
    Raises Exception if database cannot be connected to.
    """
    base_dir = Path(__file__).parent.parent
    db_path = base_dir / "mydict.db"
    
    try:
        conn = sqlite3.connect(str(db_path))
        # Test the connection by querying the LEMMA table
        cursor = conn.execute("SELECT COUNT(*) FROM LEMMA")
        count = cursor.fetchone()[0]
        print(f"Tilkobling til databasen vellykket. Fant {count} oppføringer i LEMMA-tabellen.")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise Exception(f"Kunne ikke koble til databasen: {e}")
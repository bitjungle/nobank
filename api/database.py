import sqlite3
from pathlib import Path
from typing import Optional

def get_db_connection() -> sqlite3.Connection:
    """
    Connect to the SQLite database, trying multiple locations.
    Returns a connection with row_factory set to sqlite3.Row.
    
    Raises Exception if database cannot be found or connected to.
    """
    base_dir = Path(__file__).parent.parent
    
    # Try database in different locations
    possible_paths = [
        base_dir / "mydict.db",
        base_dir.parent / "mydict.db",
        base_dir / "src" / "mydict.db",
    ]
    
    last_error = None
    for db_path in possible_paths:
        try:
            conn = sqlite3.connect(str(db_path))
            # Test the connection by querying the LEMMA table
            cursor = conn.execute("SELECT COUNT(*) FROM LEMMA")
            count = cursor.fetchone()[0]
            print(f"Tilkobling til databasen {db_path} vellykket. Fant {count} oppføringer i LEMMA-tabellen.")
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            last_error = e
            continue
            
    # If we get here, we couldn't connect to the database
    raise Exception(f"Kunne ikke koble til databasen. Sørg for at mydict.db eksisterer. Siste feil: {last_error}")
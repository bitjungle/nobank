import pandas as pd
import sqlite3
import os
from pathlib import Path

# Get database path from environment variable or use default paths
db_path = os.environ.get("DB_PATH", "data/mydict.db")
if not Path(db_path).exists():
    if Path("mydict.db").exists():
        db_path = "mydict.db"
    elif Path("../mydict.db").exists():
        db_path = "../mydict.db"

print(f"📊 Bruker database: {db_path}")
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = ON;")

files = {
    "src/ordbank/boying_grupper.txt": "BOYING_GRUPPER",
    "src/ordbank/lemma.txt": "LEMMA",
    "src/ordbank/paradigme.txt": "PARADIGME",
    "src/ordbank/boying.txt": "BOYING",
    "src/ordbank/paradigme_boying.txt": "PARADIGME_BOYING",
    "src/ordbank/lemma_paradigme.txt": "LEMMA_PARADIGME",
    "src/ordbank/fullformsliste.txt": "FULLFORMSLISTE",
    "src/ordbank/leddanalyse.txt": "LEDDANALYSE"
}

int_columns = {"LEMMA_ID", "PARADIGME_ID", "BOY_NUMMER", "LEDDANALYSE_ID", "ID"}
date_columns = {"FRADATO", "TILDATO"}

try:
    for file_path, table in files.items():
        if not Path(file_path).exists():
            print(f"⚠️  Filen finnes ikke: {file_path}")
            continue

        print(f"\n📥 Importerer {file_path} → {table}")
        df = pd.read_csv(
            file_path,
            sep="\t",
            dtype=str,
            keep_default_na=False,
            na_values=[]
        )

        df.columns = [col.strip("'").strip() for col in df.columns]
        df.drop(columns=[col for col in df.columns if col.upper() == 'LOEPENR'], inplace=True, errors='ignore')

        for col in df.columns:
            if col in int_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")
            elif col in date_columns:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.date

        df.to_sql(table, conn, if_exists='append', index=False)
        print(f"✅ {len(df)} rader lagt til i {table}")

finally:
    conn.close()
    print("\n🔒 Forbindelsen til databasen er lukket.")

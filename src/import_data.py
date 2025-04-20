import pandas as pd
import sqlite3
from pathlib import Path

conn = sqlite3.connect("mydict.db")
conn.execute("PRAGMA foreign_keys = ON;")

files = {
    "ordbank/boying_grupper.txt": "BOYING_GRUPPER",
    "ordbank/lemma.txt": "LEMMA",
    "ordbank/paradigme.txt": "PARADIGME",
    "ordbank/boying.txt": "BOYING",
    "ordbank/paradigme_boying.txt": "PARADIGME_BOYING",
    "ordbank/lemma_paradigme.txt": "LEMMA_PARADIGME",
    "ordbank/fullformsliste.txt": "FULLFORMSLISTE",
    "ordbank/leddanalyse.txt": "LEDDANALYSE"
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

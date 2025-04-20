import pandas as pd

# Last inn filer
fullform = pd.read_csv("ordbank/fullformsliste.txt", sep="\t", dtype=str)
paradigme_boying = pd.read_csv("ordbank/paradigme_boying.txt", sep="\t", dtype=str)
boying = pd.read_csv("ordbank/boying.txt", sep="\t", dtype=str)
boying_grupper = pd.read_csv("ordbank/boying_grupper.txt", sep="\t", dtype=str)

# Behold kun relevante kolonner og unngå duplikater
paradigme_boying_clean = paradigme_boying[["PARADIGME_ID", "BOY_NUMMER", "BOY_GRUPPE"]].drop_duplicates()

# Slå sammen for å hente inn BOY_GRUPPE
fullform_beriket = fullform.merge(
    paradigme_boying_clean,
    how="left",
    on=["PARADIGME_ID", "BOY_NUMMER"]
)

# Filtrer ut rader der BOY_GRUPPE ikke ble funnet
manglende = fullform_beriket[fullform_beriket["BOY_GRUPPE"].isna()]

# Resultater
print(f"❌ Antall rader uten gyldig BOY_GRUPPE: {len(manglende)}")
print("\n📋 Eksempler på rader med manglende BOY_GRUPPE:")
print(manglende[["PARADIGME_ID", "BOY_NUMMER", "OPPSLAG", "TAG"]].drop_duplicates().head(10))

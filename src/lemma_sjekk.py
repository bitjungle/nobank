import pandas as pd

# fullformsliste.txt inneholder fraser, idiomer, forkortelser, symboler, etc., 
# som ikke nødvendigvis har (eller bør ha) egne lemma-oppføringer.

lemma = pd.read_csv("ordbank/lemma.txt", sep="\t", dtype=str, index_col='LOEPENR')
fullformsliste = pd.read_csv("ordbank/fullformsliste.txt", sep="\t", dtype=str, index_col='LOEPENR')
invalid_lemmas = fullformsliste[~fullformsliste["LEMMA_ID"].isin(lemma["LEMMA_ID"])]

print("❌ Rader i fullformsliste med manglende LEMMA_ID:")
print(invalid_lemmas)

# lemma_paradigme.txt inneholder en LEMMA_ID som ikke finnes i lemma.txt.

lemma_paradigme = pd.read_csv("ordbank/lemma_paradigme.txt", sep="\t", dtype=str)

# Finn hvilke ID-er som er problemet
invalid_lemmas = lemma_paradigme[~lemma_paradigme["LEMMA_ID"].isin(lemma["LEMMA_ID"])]

print("Ugyldige LEMMA_ID:", invalid_lemmas["LEMMA_ID"].unique())

import sqlite3

def hent_boyinger(ordform: str, ordklasse: str):
    conn = sqlite3.connect("../mydict.db")
    conn.row_factory = sqlite3.Row

    query = """
    SELECT DISTINCT
        f.OPPSLAG,
        f.TAG,
        b.BOY_TEKST,
        b.ORDBOK_TEKST
    FROM
        LEMMA l
    JOIN FULLFORMSLISTE f ON l.LEMMA_ID = f.LEMMA_ID
    LEFT JOIN PARADIGME_BOYING pb
        ON f.PARADIGME_ID = pb.PARADIGME_ID AND f.BOY_NUMMER = pb.BOY_NUMMER
    LEFT JOIN BOYING b
        ON pb.BOY_NUMMER = b.BOY_NUMMER AND pb.BOY_GRUPPE = b.BOY_GRUPPE
    WHERE
        l.GRUNNFORM = ?
        AND f.NORMERING = 'normert'
        AND f.TAG LIKE ? || '%'
    ORDER BY f.OPPSLAG;
    """

    rows = conn.execute(query, (ordform, ordklasse)).fetchall()
    conn.close()
    return rows

def vis_resultat(ordform: str, ordklasse: str, rows):
    if not rows:
        print(f"❌ Fant ingen normerte bøyningsformer for '{ordform}' ({ordklasse})")
    else:
        print(f"\n📖 Bøyningsformer for '{ordform}' ({ordklasse}):\n")
        for row in rows:
            print(f"  - {row['OPPSLAG']:15} {row['TAG'] or '':35} ({row['BOY_TEKST'] or '?'} → {row['ORDBOK_TEKST'] or '?'})")

def velg_ordklasse():
    print("📚 Velg ordklasse:")
    print("  1. verb")
    print("  2. substantiv (subst)")
    print("  3. avslutt")

    valg = input("👉 Ditt valg (1–3): ").strip()
    return {
        "1": "verb",
        "2": "subst",
        "3": "exit"
    }.get(valg)

if __name__ == "__main__":
    print("🔍 Norsk Ordbank CLI – slå opp bøyningsformer")
    print("---------------------------------------------")

    while True:
        ordklasse = velg_ordklasse()
        if ordklasse == "exit":
            print("👋 Avslutter.")
            break
        if ordklasse not in {"verb", "subst"}:
            print("⚠️  Ugyldig valg. Prøv igjen.\n")
            continue

        ordform = input("📥 Oppgi grunnform: ").strip()
        if not ordform:
            print("⚠️  Du må skrive inn et ord.\n")
            continue

        resultat = hent_boyinger(ordform, ordklasse)
        vis_resultat(ordform, ordklasse, resultat)
        print()

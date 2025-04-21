# nobank - Norsk ordbank (bokmål) med verktøy

[![License: CC BY 4.0](https://img.shields.io/badge/data_license-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/) 
[![License: MIT](https://img.shields.io/badge/code_license-MIT-green.svg)](LICENSE)
[![Made with Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue.svg)](https://sqlite.org/index.html)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)

Et prosjekt som gjør Nasjonalbibliotekets *Norsk Ordbank* søkbar via en lokal SQLite-database – komplett med databasemodell, importscript, et enkelt CLI-verktøy og REST API for oppslag av bøyningsformer.

---

## Innhold

- [nobank - Norsk ordbank (bokmål) med verktøy](#nobank---norsk-ordbank-bokmål-med-verktøy)
  - [Innhold](#innhold)
  - [Om Ordbanken](#om-ordbanken)
  - [Prosjektstruktur](#prosjektstruktur)
  - [Datamodell og designvalg](#datamodell-og-designvalg)
    - [Hovedvalg og kompromisser](#hovedvalg-og-kompromisser)
    - [Viktige tabeller](#viktige-tabeller)
  - [Krav](#krav)
    - [Python](#python)
    - [SQLite](#sqlite)
  - [Installasjon og bruk](#installasjon-og-bruk)
    - [1. Last ned eller klone `nobank` fra GitHub:](#1-last-ned-eller-klone-nobank-fra-github)
    - [2. Sett opp virtuelt miljø og installer avhengigheter:](#2-sett-opp-virtuelt-miljø-og-installer-avhengigheter)
    - [3. Opprett databasen:](#3-opprett-databasen)
  - [Demo CLI: Interaktivt oppslag](#demo-cli-interaktivt-oppslag)
  - [REST API](#rest-api)
    - [Starte API-serveren](#starte-api-serveren)
    - [Endepunkter](#endepunkter)
    - [Eksempler](#eksempler)
  - [Kilder og lisens](#kilder-og-lisens)

---

## Om Ordbanken

Dette prosjektet bruker [Norsk Ordbank](https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-5/) levert av [Nasjonalbiblioteket](https://www.nb.no/).  
Ordbanken er en omfattende leksikalsk ressurs som inneholder over 150 000 lemmaer, bøyningsparadigmer og over 1 million bøyningsformer.

---

## Prosjektstruktur

```
.
├── Makefile               # Automatiserer databaseoppsett og import
├── mydict.db              # SQLite-databasen (genereres)
├── api/                   # REST API for ordbanken
│   ├── routes/            # API-endepunkter
│   ├── main.py            # FastAPI-applikasjon
│   ├── models.py          # Datamodeller
│   ├── database.py        # Databasehåndtering
│   └── run.py             # Server startup script
├── src/
│   ├── ordbank/*          # Mappe med originaldata fra Språkbanken (.txt)
│   ├── schema.sql         # SQL-skjema (DDL)
│   ├── import_data.py     # Import av alle datafiler
│   ├── sjekk_boy.py       # Hjelpeskript brukt under utvikling av SQL skjema
│   ├── sjekk_lemma.py     # Hjelpeskript brukt under utvikling av SQL skjema
│   └── test_oppslag.py    # CLI-app for bøyningsoppslag, for demo og testing
└── README.md              # Denne filen
```

---

## Datamodell og designvalg

Datamodellen er laget med utgangspunkt i strukturen i ordbankens `.txt`-filer fra Nasjonalbiblioteket. Disse ligger i [src/ordbank](src/ordbank/) og har blitt konvertert fra det opprinnelige `Windows 1252`-formatet til `UTF-8`. Filene er ellers uendret.

### Hovedvalg og kompromisser

- `FULLFORMSLISTE` inkluderer ikke `FOREIGN KEY` til `BOYING`, fordi ikke alle `BOY_NUMMER`-verdier kan matches entydig mot en `BOY_GRUPPE`.
- `LEMMA_ID` i `FULLFORMSLISTE` er ikke en `FOREIGN KEY` for samme grunn – enkelte rader er knyttet til sammensatte uttrykk eller ufullstendige lemma.

### Viktige tabeller

- `LEMMA`: grunnformer
- `FULLFORMSLISTE`: alle bøyningsformer
- `PARADIGME`, `PARADIGME_BOYING`, `BOYING`: definerer bøyningssystem
- `LEDDANALYSE`: informasjon om leddstruktur i sammensatte ord

---

## Krav

- Python ≥ 3.12
- `sqlite3`


### Python

Installer nødvendige Python-pakker med pip:

```bash
pip install -r requirements.txt
```

### SQLite

Du trenger også `sqlite3` for å opprette og bruke databasen.

| Plattform | Installasjon |
|-----------|--------------|
| **macOS** | Allerede installert |
| **Linux** | Bruk pakkebehandler:<br>`sudo apt install sqlite3`<br>eller<br>`sudo dnf install sqlite` |
| **Windows** | Last ned fra:<br>[https://sqlite.org/download.html](https://sqlite.org/download.html)<br><br>Velg **"sqlite-tools" ZIP** under *Precompiled Binaries for Windows*<br><br>Pakk ut og legg `sqlite3.exe` i en mappe som ligger i `PATH` |

---

## Installasjon og bruk

### 1. Last ned eller klone `nobank` fra GitHub:

```bash
git clone git@github.com:bitjungle/nobank.git
```

### 2. Sett opp virtuelt miljø og installer avhengigheter:

```bash
make venv requirements
```

Dette oppretter et virtuelt Python-miljø i `venv`-mappen og installerer alle nødvendige pakker.

### 3. Opprett databasen:

```bash
make schema import
```

---

## Demo CLI: Interaktivt oppslag

```bash
python src/test_oppslag.py
```

Velg ordklasse og oppgi et ord:

```
---------------------------------------------
📚 Velg ordklasse:
  1. verb
  2. substantiv (subst)
  3. avslutt
👉 Ditt valg (1–3): 2
📥 Oppgi grunnform: bil

📖 Bøyningsformer for 'bil' (subst):

  - bil             subst mask appell ent ub normert    (ent ub → entall_ubestemt)
  - bilen           subst mask appell ent be normert    (ent be → entall_bestemt)
  - bilene          subst mask appell fl be normert     (fl be → flertall_bestemt)
  - biler           subst mask appell fl ub normert     (fl ub → flertall_ubestemt)
  ...
```

## REST API

Prosjektet inkluderer også et REST API bygget med [FastAPI](https://fastapi.tiangolo.com/) som gir enkel tilgang til ordbankens innhold fra andre applikasjoner.

### Starte API-serveren

```bash
make api
```

Denne kommandoen vil bruke det virtuelle miljøet og starte API-serveren på http://127.0.0.1:8000

### Endepunkter

| Endepunkt | Beskrivelse | Parametre |
|-----------|-------------|-----------|
| `/api/words/{word}` | Henter alle bøyningsformer for et ord | `ordklasse` (valgfri): Filter på ordklasse (f.eks. "verb", "subst") |
| `/api/search/` | Søker etter ord som starter med en bestemt streng | `q`: Søkestreng<br>`limit` (valgfri): Maks antall resultater (standard: 10) |
| `/api/ordklasser/` | Lister opp alle tilgjengelige ordklasser | - |
| `/docs` | Interaktiv API-dokumentasjon | - |
| `/redoc` | Alternativ API-dokumentasjon | - |

### Eksempler

1. **Hent alle bøyningsformer for et ord**:
   ```
   GET /api/words/bil
   ```

2. **Hent alle bøyningsformer for et verb**:
   ```
   GET /api/words/løpe?ordklasse=verb
   ```

3. **Søk etter ord**:
   ```
   GET /api/search/?q=bil&limit=20
   ```

---

## Kilder og lisens

- **Data**: [Norsk Ordbank – Språkbanken/NB](https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-5/)  
  Lisensiert under [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/) – fri bruk med kreditering til [Nasjonalbiblioteket](https://www.nb.no/)
- **Kode**: Alt Python-innhold i dette prosjektet er lisensiert under [MIT-lisensen](LICENSE)

---

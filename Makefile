DB = mydict.db
SCHEMA = src/schema.sql
IMPORT = src/import_data.py
API = api/run.py

.PHONY: all schema import clean api

# Standardregel: sett opp database og importer data
all: schema import

# Kjør schema.sql mot SQLite-databasen
schema:
	sqlite3 $(DB) < $(SCHEMA)

# Kjør Python-importen
import:
	python $(IMPORT)

# Slett databasen (valgfritt)
clean:
	rm -f $(DB)

# Start API-serveren
api:
	python $(API)

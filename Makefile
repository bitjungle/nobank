DB = mydict.db
SCHEMA = src/schema.sql
IMPORT = src/import_data.py

.PHONY: all schema import clean

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

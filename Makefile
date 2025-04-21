DB = mydict.db
SCHEMA = src/schema.sql
IMPORT = src/import_data.py
API = api/run.py
VENV = .venv
PYTHON_HOST_COMPUTER = python3
PIP = $(VENV)/bin/pip

.PHONY: all schema import clean api venv requirements

# Standardregel: sett opp virtuelt miljø, database og importer data
all: venv requirements schema import

# Kjør schema.sql mot SQLite-databasen
schema:
	sqlite3 $(DB) < $(SCHEMA)

# Kjør Python-importen
import: venv
	python $(IMPORT)

# Start API-serveren
api: venv
	python $(API)

# Opprett virtuelt Python-miljø
venv:
	test -d $(VENV) || $(PYTHON_HOST_COMPUTER) -m venv $(VENV)
	touch $(VENV)

# Installer nødvendige pakker i virtuelt miljø
requirements: venv
	$(PIP) install -r requirements.txt

# Slett databasen
clean:
	rm -f $(DB)

# Start på nytt med rent miljø (slett venv og database)
clean-all: clean
	rm -rf $(VENV)

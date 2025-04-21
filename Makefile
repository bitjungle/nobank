DB = mydict.db
SCHEMA = src/schema.sql
IMPORT = src/import_data.py
API = api/run.py
VENV = .venv
PYTHON_HOST_COMPUTER = python3
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
DOCKER_IMAGE = nobank-api

.PHONY: all schema import clean api venv requirements docker docker-run docker-build

# Standardregel: sett opp virtuelt miljø, database og kjører api-server
all: venv requirements schema import api

# Kjør schema.sql mot SQLite-databasen
schema:
	sqlite3 $(DB) < $(SCHEMA)

# Kjør Python-importen
import: venv
	$(PYTHON) $(IMPORT)

# Start API-serveren
api: venv
	$(PYTHON) $(API)

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

# Bygg Docker-image
docker-build:
	docker build -t $(DOCKER_IMAGE) .

# Kjør Docker-container
docker-run:
	docker run -p 8000:8000 --name $(DOCKER_IMAGE) $(DOCKER_IMAGE)

# Bygg og kjør Docker (alt-i-ett)
docker: docker-build docker-run

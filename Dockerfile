FROM python:3.12-slim

# Sett arbeidskatalog i containeren
WORKDIR /app

# Kopier kodebasen og avhengigheter
COPY requirements.txt .
COPY api/ ./api/
COPY src/ ./src/
COPY README.md .
COPY LICENSE .
COPY mydict.db .

# Installer avhengigheter
RUN pip install --no-cache-dir -r requirements.txt

# Eksponer port for API-serveren
EXPOSE 8000

# Sett miljøvariabler for containeren
ENV PYTHONUNBUFFERED=1

# Start API-serveren ved kjøring av containeren
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# Start API-serveren ved kjøring av containeren
ENTRYPOINT ["./docker-entrypoint.sh"]
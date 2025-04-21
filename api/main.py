from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import words

app = FastAPI(
    title="Norsk Ordbank API",
    description="API for norsk bokmål ordbok basert på Nasjonalbibliotekets Ordbank",
    version="1.0.0"
)

# Add CORS middleware to allow requests from web applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(words.router, prefix="/api", tags=["words"])

@app.get("/", tags=["status"])
def read_root():
    return {
        "status": "online",
        "message": "Norsk Ordbank API er klar til bruk",
        "docs": "/docs"
    }
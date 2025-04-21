#!/bin/bash
set -e

echo "🚀 Starting API server..."
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
#!/bin/sh
# Use PORT from Cloud Run, default to 8080 if not set
exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8080}

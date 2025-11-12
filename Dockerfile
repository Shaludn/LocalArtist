# Use official Python image (3.12-slim is a great choice)
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install requirements
# This step should be done first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
# This copies your backend/ directory, main.py, etc.
COPY . .

# Expose port 8080 (optional but good practice)
EXPOSE 8080

# Production Start Command (CMD)
# Using the shell form (CMD string) ensures the $PORT variable is correctly interpolated
# by the shell before Gunicorn is executed.
# This fixes the "$PORT is not a valid port number" error.
# 
# IMPORTANT: Ensure 'backend.main:app' matches your file structure:
#   - 'backend' is the folder/module name
#   - 'main' is the file inside 'backend' (i.e., backend/main.py)
#   - 'app' is the FastAPI instance name (i.e., app = FastAPI())
CMD gunicorn backend.main:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker --workers 2 --timeout 60

## 🚀 Next Steps: Rebuild and Redeploy


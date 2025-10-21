# Use official Python image
FROM python:3.12-slim

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Copy entrypoint script and make it executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expose port 8080
EXPOSE 8080

# Use entrypoint script as CMD
CMD ["./entrypoint.sh"]

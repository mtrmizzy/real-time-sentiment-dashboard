# Use official Python image as base
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy your local code into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default command to run script
CMD ["python", "ingest.py"]
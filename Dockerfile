# Use a lightweight Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies (if any are needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Initialize the Hugging Face model during the build process
RUN python3 -c "from transformers import pipeline; pipeline('text-classification', model='Hate-speech-CNERG/dehatebert-mono-english')"

# Expose the port the app runs on
EXPOSE 7000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]
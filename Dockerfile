# Use the latest Ubuntu as the base image
FROM ubuntu:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate the virtual environment and upgrade pip
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies in the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 7000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]
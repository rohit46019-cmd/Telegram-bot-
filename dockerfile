# Use Python 3.11 slim image (stable, has prebuilt wheels for pydantic-core & tgcrypto)
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies (optional but helps with some Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip tooling to ensure wheels are used
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port for FastAPI health-check (Render fix)
EXPOSE 10000

# Start the bot
CMD ["python", "main.py"]
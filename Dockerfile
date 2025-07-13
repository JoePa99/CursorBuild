# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade "pip<24.1" && pip install -r requirements.txt

# Copy application code
COPY main.py .
COPY railway.toml .
COPY runtime.txt .

# Expose port
EXPOSE 8000

# Set environment variable
ENV PORT=8000

# Start the application
CMD ["python", "main.py"] 
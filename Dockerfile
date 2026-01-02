# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    CUDA_VISIBLE_DEVICES=-1

# Install system dependencies required for OpenCV and DeepFace
# libgl1 and libglib2.0-0 are critical for import cv2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a writable directory for DeepFace weights to avoid permission issues if needed
# DeepFace downloads weights to ~/.deepface by default.
# We create it and set permissions just in case we run as non-root later, 
# though running as root in container is standard for this simple setup.
RUN mkdir -p /root/.deepface/weights

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Default command uses gunicorn for production
# 2 workers recommended for basic load, increase based on resources
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "run:app"]

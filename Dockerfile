# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    CUDA_VISIBLE_DEVICES=-1

# Install system dependencies required for OpenCV and DeepFace
# libgl1 and libglib2.0-0 are critical for import cv2
# curl is needed to download weights
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Pre-download DeepFace models to bake into image (prevents runtime timeouts)
# We need: age_model_weights.h5 (~540MB)
# PLACED BEFORE REQUIREMENTS to utilize Docker cache (requirements change often, models don't)
RUN mkdir -p /root/.deepface/weights && \
    if [ ! -f "/root/.deepface/weights/age_model_weights.h5" ]; then \
        echo "Downloading Age Model..." && \
        curl -L "https://github.com/serengil/deepface_models/releases/download/v1.0/age_model_weights.h5" -o /root/.deepface/weights/age_model_weights.h5; \
    else \
        echo "Age Model exists. Skipping."; \
    fi

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Default command uses gunicorn for production
# Increased timeout for model loading
# --preload to share model memory across workers (saves RAM)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "300", "--preload", "run:app"]

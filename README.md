# Flask DeepFace API

A simple, Dockerized REST API for face detection and attribute analysis (Age, Emotion) using [DeepFace](https://github.com/serengil/deepface) and Flask.

## Features
- **Face Detection**: Returns bounding box coordinates.
- **Attribute Analysis**: Estimates age and dominant emotion.
- **No Recognition**: Purely detection and analysis (privacy-friendly for basic presence checks).
- **Dockerized**: specific dependencies installed for a smooth run.

## Project Structure
```text
flask-deepface/
  app/
    __init__.py
    routes.py
    services/
      deepface_service.py
    utils/
      validators.py
      responses.py
    config.py
  run.py
  requirements.txt
  README.md
  .env.example
  Dockerfile
  docker-compose.yml
```

## Setup & Running

### 1. Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```
Edit `.env` if needed:
- `API_KEY`: Set your secret key for authentication.
- `DETECTOR_BACKEND`: `opencv` (default, fast), `retinaface` (slower, more accurate), etc.
- `MAX_IMAGE_MB`: Max upload size in MB.

### 2. Run with Docker (Recommended)
This is the most reliable method as it handles system dependencies (GL libs).

```bash
docker compose up --build
```

The service will start at `http://localhost:5000`.

> **Note**: The first run might take a minute or two to download the DeepFace weights inside the container if they are not cached.

### 3. Run Manually (Optional)
Ensure you have Python 3.11+ and system libraries for OpenCV installed.

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python run.py
```

## API Endpoints

### 1. Health Check
Check operational status.

- **URL**: `/health`
- **Method**: `GET`
- **Success Response (200)**:
```json
{
  "status": "ok",
  "service": "flask-deepface",
  "version": "1.0.0",
  "time": "2023-10-27T10:00:00"
}
```

### 2. Detect Faces
Upload an image to detect faces and analyze attributes.

- **URL**: `/detect`
- **Method**: `POST`
- **Headers**: 
  - `Content-Type: multipart/form-data`
  - `x-api-key`: <YOUR_API_KEY> **[Required]**
- **Body**:
  - `image`: File (jpg, jpeg, png) OR URL string (http/https) **[Required]**

#### Success Response (200) - Face Detected
```json
{
  "status": "success",
  "faces_count": 1,
  "faces": [
    {
      "bbox": { "x": 100, "y": 50, "w": 200, "h": 200 },
      "age": 28,
      "dominant_emotion": "happy",
      "emotion": { "happy": 99.5, "sad": 0.1, ... },
      "confidence": 0.98
    }
  ],
  "meta": {
    "timestamp": "...",
    "detector_backend": "opencv"
  }
}
```

#### Example Usage
**File Upload:**
```bash
curl -X POST http://localhost:5000/detect \
  -F "image=@/path/to/photo.jpg"
```

**URL:**
```bash
curl -X POST http://localhost:5000/detect \
  -F "image=https://raw.githubusercontent.com/serengil/deepface/master/tests/dataset/img1.jpg"
```

#### Failure Response (422) - No Face Detected
Used for presence logic when no face is found in the uploaded photo.
```json
{
  "status": "failed",
  "reason": "no_face_detected",
  "message": "Tidak ada wajah terdeteksi pada foto. Presensi gagal.",
  "meta": { ... }
}
```

#### Error Responses
- **400 Bad Request**: Missing file/URL or invalid input.
- **413 Content Too Large**: File > MAX_IMAGE_MB.
- **415 Unsupported Media Type**: Not a jpg/png.
- **500 Internal Server Error**: Server processing error.

## Notes
- **Models**: DeepFace downloads weights to `/root/.deepface/weights` in the container. To persist them, uncomment the volume mapping in `docker-compose.yml`.
- **Backend**: `opencv` is fastest but less accurate. Switch to `retinaface` in `.env` for better detection integration if needed (requires internet on first run to download retinaface weights).
- **CPU Optimized**: Configured to run on CPU only (`CUDA_VISIBLE_DEVICES=-1`) to save resources.

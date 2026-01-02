# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-01-02

### Added
- Initial release of **flask-deepface**.
- Docker support with `Dockerfile` and `docker-compose.yml`.
- Face detection service using `DeepFace` library.
- **API Endpoints**:
  - `GET /health`: Service health check.
  - `POST /detect`: Face detection and attribute analysis (age, emotion).
- **Features**:
  - Support for image file uploads (multipart/form-data).
  - Support for image URLs in `image` field.
  - CPU-only optimization (`CUDA_VISIBLE_DEVICES=-1`).
  - Configurable backend (default: `opencv`) via environment variables.
  - Strict input validation (MIME type, size).
- **Documentation**:
  - Comprehensive `README.md`.
  - Project meta files (`.gitignore`, `.dockerignore`).

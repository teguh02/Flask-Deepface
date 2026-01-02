import io
import requests
from flask import Blueprint, request, current_app
from datetime import datetime
from app.utils.responses import success_response, error_response
from app.utils.validators import validate_image_request
from app.utils.auth import require_api_key
from app.services.deepface_service import DeepFaceService
from app.config import Config

main_bp = Blueprint('main', __name__)

@main_bp.route('/health', methods=['GET'])
def health():
    return success_response({
        "service": "flask-deepface",
        "version": "1.0.0",
        "time": datetime.now().isoformat()
    }, status_code=200)

@main_bp.route('/detect', methods=['POST'])
@require_api_key
def detect():
    # 1. Validate Input
    is_valid, error_reason, error_msg, status_code = validate_image_request(request)
    if not is_valid:
        return error_response(
            reason=error_reason,
            message=error_msg,
            status_code=status_code,
            meta={
                "timestamp": datetime.now().isoformat(),
                "detector_backend": Config.DETECTOR_BACKEND
            }
        )

    # 2. Get Image Data
    image_file = None
    try:
        if 'image' in request.files:
            image_file = request.files['image']
        elif 'image' in request.form:
            # Download URL
            url = request.form['image']
            # Timeout set to 15s to avoid hanging
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            image_file = io.BytesIO(resp.content)
    except requests.exceptions.RequestException as e:
        return error_response(
            reason="download_failed",
            message=f"Gagal mengunduh gambar dari URL: {str(e)}",
            status_code=400
        )

    try:
        # 3. Process with DeepFace
        faces = DeepFaceService.detect_and_analyze(image_file)
        
        # 4. Return Success
        return success_response({
            "faces_count": len(faces),
            "faces": faces,
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "detector_backend": Config.DETECTOR_BACKEND
            }
        }, status_code=200)

    except ValueError as e:
        # Special handling for "No face detected"
        if "No face detected" in str(e) or "Face could not be detected" in str(e):
             return error_response(
                reason="no_face_detected",
                message="Tidak ada wajah terdeteksi pada foto.",
                status_code=422,
                meta={
                    "timestamp": datetime.now().isoformat(),
                    "detector_backend": Config.DETECTOR_BACKEND
                }
            )
        # Other ValueErrors (e.g. decoding)
        current_app.logger.error(f"ValueError: {e}")
        return error_response(
            reason="processing_error",
            message="Gagal memproses gambar.",
            status_code=400,
            meta={"details": str(e)}
        )

    except Exception as e:
        current_app.logger.error(f"System Error: {e}")
        return error_response(
            reason="internal_error",
            message="Terjadi kesalahan pada server.",
            status_code=500,
            meta={"timestamp": datetime.now().isoformat()}
        )

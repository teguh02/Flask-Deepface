import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # DeepFace Settings
    DETECTOR_BACKEND = os.getenv('DETECTOR_BACKEND', 'opencv')
    # Parse boolean for ENFORCE_DETECTION
    ENFORCE_DETECTION = os.getenv('ENFORCE_DETECTION', 'true').lower() == 'true'
    
    # Upload Settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_IMAGE_MB', 5)) * 1024 * 1024  # Flask built-in limit
    MAX_IMAGE_MB = int(os.getenv('MAX_IMAGE_MB', 5))
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Supported extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

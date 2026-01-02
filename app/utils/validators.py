from werkzeug.datastructures import FileStorage
from app.config import Config

def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_image_request(request):
    """
    Validates the existence, type, and size of the image in the request.
    Returns (Tuple): (is_valid, error_reason, error_message, status_code)
    """
    # 1. Check for File Upload
    if 'image' in request.files:
        file = request.files['image']
        if file.filename == '':
            return False, "missing_filename", "No selected file.", 400
        if not allowed_file(file.filename):
            return False, "invalid_file_type", f"Allowed file types are: {', '.join(Config.ALLOWED_EXTENSIONS)}", 415
        return True, None, None, 200

    # 2. Check for URL in Form Data
    elif 'image' in request.form:
        url = request.form['image']
        if not url:
            return False, "missing_url", "URL cannot be empty.", 400
        if not (url.startswith('http://') or url.startswith('https://')):
             return False, "invalid_url_scheme", "URL must start with http:// or https://", 400
        return True, None, None, 200

    # 3. Missing Both
    else:
        return False, "missing_field", "Field 'image' (file or valid URL) is required.", 400

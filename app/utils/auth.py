from functools import wraps
from flask import request, current_app
from app.config import Config
from app.utils.responses import error_response

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = Config.API_KEY
        
        # If no API Key is configured in env, skip check (or fail secure, but usually dev mode allows. 
        # Requirement implies strict usage, so we enforce if set)
        if not api_key:
            return f(*args, **kwargs)

        # Check header
        request_key = request.headers.get('x-api-key')
        
        if not request_key:
            return error_response(
                reason="missing_api_key",
                message="API Key is missing. Please provide 'x-api-key' header.",
                status_code=401
            )
            
        if request_key != api_key:
            return error_response(
                reason="invalid_api_key",
                message="Invalid API Key provided.",
                status_code=403
            )
            
        return f(*args, **kwargs)
    return decorated_function

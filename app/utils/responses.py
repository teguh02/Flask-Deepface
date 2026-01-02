from flask import jsonify
from datetime import datetime

def success_response(data: dict, message: str = "Success", status_code: int = 200):
    response = {
        "status": "success",
        "message": message,
        **data
    }
    return jsonify(response), status_code

def error_response(reason: str, message: str, meta: dict = None, status_code: int = 400):
    """
    Standard error response format.
    Used for 4xx and 5xx errors.
    """
    response = {
        "status": "failed",
        "reason": reason,
        "message": message,
        "meta": meta or {}
    }
    # Ensure timestamp is in meta if not provided, though usually passed by caller
    if "timestamp" not in response["meta"]:
        response["meta"]["timestamp"] = datetime.now().isoformat()
        
    return jsonify(response), status_code

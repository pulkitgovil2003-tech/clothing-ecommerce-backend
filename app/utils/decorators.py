from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

def admin_required(fn):
    """Decorator to allow only admin users"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"message": "Admins only!"}), 403
        return fn(*args, **kwargs)
    return wrapper
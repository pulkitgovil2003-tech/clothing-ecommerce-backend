from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps
from flask import jsonify

def get_current_user_id():
    """Get the current logged-in user ID from JWT token"""
    return get_jwt_identity()
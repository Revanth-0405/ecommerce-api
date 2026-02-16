from flask import request
from app.models.api_key_model import APIKey
from app.services.rate_limit_service import check_rate_limit
from app.utils.error_handler import error_response
from app.config import Config
import hashlib


def require_api_key(role=None):

    def decorator(func):

        def wrapper(*args, **kwargs):

            key = request.headers.get("X-API-Key")

            # Missing key
            if not key:
                return error_response("Missing API Key", "AUTH001", 401)

            hashed = hashlib.sha256(key.encode()).hexdigest()

            record = APIKey.query.filter_by(key=hashed).first()

            # Invalid key
            if not record or not record.is_active:
                return error_response("Invalid API Key", "AUTH002", 403)

            # Role check
            if role and record.role != role:
                return error_response("Permission denied", "AUTH003", 403)

            # Rate limit
            if not check_rate_limit(hashed, Config.RATE_LIMIT):
                return error_response("Rate limit exceeded", "RATE001", 429)

            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator

import hashlib
import secrets
from app.models.api_key_model import APIKey
from app.db import db

def generate_api_key(owner, role):
    raw = secrets.token_hex(32)
    hashed = hashlib.sha256(raw.encode()).hexdigest()

    key = APIKey(key=hashed, owner=owner, role=role)
    db.session.add(key)
    db.session.commit()

    return raw

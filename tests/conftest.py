import pytest
import hashlib
from run import app
from app.db import db
from app.models.api_key_model import APIKey


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


@pytest.fixture
def admin_key(client):
    key = "ADMIN123"
    hashed = hashlib.sha256(key.encode()).hexdigest()

    with app.app_context():
        record = APIKey(
            key=hashed,
            owner="test_admin",
            role="admin"
        )
        db.session.add(record)
        db.session.commit()

    return key


@pytest.fixture
def user_key(client):
    key = "USER123"
    hashed = hashlib.sha256(key.encode()).hexdigest()

    with app.app_context():
        record = APIKey(
            key=hashed,
            owner="test_user",
            role="viewer"
        )
        db.session.add(record)
        db.session.commit()

    return key

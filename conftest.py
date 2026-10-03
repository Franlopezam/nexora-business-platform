import os
os.environ["DATABASE_URL"] = "sqlite:///./test_nexora.db"
os.environ["SECRET_KEY"] = "test-secret"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine, SessionLocal
from app.models.user import User
from app.security.auth import hash_password


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add(User(
        name="Test Admin",
        email="admin@test.local",
        password_hash=hash_password("Test123!"),
        role="admin",
    ))
    db.commit()
    db.close()
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

"""
Unit tests for authentication functions and API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.auth import hash_password, verify_password

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


class TestPasswordHashing:
    def test_hash_password_returns_different_value(self):
        password = "mysecretpassword"
        hashed = hash_password(password)
        assert hashed != password

    def test_verify_password_correct(self):
        password = "mysecretpassword"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        password = "mysecretpassword"
        hashed = hash_password(password)
        assert verify_password("wrongpassword", hashed) is False


class TestRegisterEndpoint:
    def test_register_success(self, client):
        response = client.post("/api/register", json={"email": "test@example.com", "username": "testuser", "password": "SecurePass123"})
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "access_token" in data

    def test_register_duplicate_email(self, client):
        client.post("/api/register", json={"email": "test@example.com", "username": "testuser", "password": "SecurePass123"})
        response = client.post("/api/register", json={"email": "test@example.com", "username": "anotheruser", "password": "AnotherPass123"})
        assert response.status_code == 400

    def test_register_short_password(self, client):
        response = client.post("/api/register", json={"email": "test@example.com", "username": "testuser", "password": "short"})
        assert response.status_code == 422


class TestLoginEndpoint:
    def test_login_success(self, client):
        client.post("/api/register", json={"email": "test@example.com", "username": "testuser", "password": "SecurePass123"})
        response = client.post("/api/login", json={"email": "test@example.com", "password": "SecurePass123"})
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, client):
        client.post("/api/register", json={"email": "test@example.com", "username": "testuser", "password": "SecurePass123"})
        response = client.post("/api/login", json={"email": "test@example.com", "password": "WrongPassword"})
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post("/api/login", json={"email": "nonexistent@example.com", "password": "SomePassword123"})
        assert response.status_code == 401

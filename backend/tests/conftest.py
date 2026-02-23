# Assigned to: Mickey (Michael Byalsky)
# Phase: 1 (B1.9)
#
# TODO: Set up pytest fixtures for backend testing.
#
# Fixtures needed:
#
# @pytest.fixture
# def db_session():
#   - Create an in-memory SQLite engine: create_engine("sqlite:///:memory:")
#   - Create all tables using Base.metadata.create_all(engine)
#   - Create a session using sessionmaker
#   - Yield the session
#   - Close session and drop all tables after test
#
# @pytest.fixture
# def client(db_session):
#   - Override the get_db dependency to return the test db_session
#   - Create a TestClient(app) from fastapi.testclient
#   - Return the test client
#
# @pytest.fixture
# def auth_headers(client):
#   - Register a test user via POST /auth/register
#       email: "testuser@my.yorku.ca", password: "testpass123", name: "Test User"
#   - Look up the verification code from the test DB (or mock email_service)
#   - Verify the user via POST /auth/verify
#   - Login via POST /auth/login
#   - Return {"Authorization": f"Bearer {access_token}"}
#
# @pytest.fixture
# def second_auth_headers(client):
#   - Same as auth_headers but with a different test user
#   - Useful for testing messaging between two users

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base
from app.dependencies import get_db
from app.main import app
from app.models.verification import VerificationCode


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database session for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a FastAPI TestClient with the test DB session override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as tc:
        yield tc
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client, db_session):
    """Register, verify, and login a test user. Return auth headers."""
    # Register
    client.post("/auth/register", json={
        "email": "testuser@my.yorku.ca",
        "password": "testpass123",
        "name": "Test User",
    })
    # Retrieve verification code from DB
    code_row = db_session.query(VerificationCode).order_by(VerificationCode.id.desc()).first()
    # Verify
    client.post("/auth/verify", json={
        "email": "testuser@my.yorku.ca",
        "code": code_row.code,
    })
    # Login
    resp = client.post("/auth/login", json={
        "email": "testuser@my.yorku.ca",
        "password": "testpass123",
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def second_auth_headers(client, db_session):
    """Register, verify, and login a second test user. Return auth headers."""
    client.post("/auth/register", json={
        "email": "testuser2@my.yorku.ca",
        "password": "testpass456",
        "name": "Test User 2",
    })
    code_row = (
        db_session.query(VerificationCode)
        .order_by(VerificationCode.id.desc())
        .first()
    )
    client.post("/auth/verify", json={
        "email": "testuser2@my.yorku.ca",
        "code": code_row.code,
    })
    resp = client.post("/auth/login", json={
        "email": "testuser2@my.yorku.ca",
        "password": "testpass456",
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

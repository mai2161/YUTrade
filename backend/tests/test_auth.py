# Assigned to: Daniel Chahine
# Phase: 1 (B1.9)
#
# TODO: Write tests for authentication endpoints.
#
# Test cases to implement:
#
# test_register_success:
#   - POST /auth/register with valid YorkU email
#   - Assert 201 status, response has "user_id" and "message"
#
# test_register_invalid_domain:
#   - POST /auth/register with non-YorkU email (e.g. "user@gmail.com")
#   - Assert 400 status
#
# test_register_duplicate_email:
#   - Register once, then register again with same email
#   - Assert 409 status on second attempt
#
# test_verify_success:
#   - Register a user, retrieve the verification code from DB
#   - POST /auth/verify with correct code
#   - Assert 200 status
#
# test_verify_wrong_code:
#   - Register a user
#   - POST /auth/verify with wrong code
#   - Assert 400 status
#
# test_login_success:
#   - Register and verify a user
#   - POST /auth/login with correct credentials
#   - Assert 200 status, response has "access_token" and "user"
#
# test_login_wrong_password:
#   - Register and verify a user
#   - POST /auth/login with wrong password
#   - Assert 401 status
#
# test_login_unverified:
#   - Register but do NOT verify
#   - POST /auth/login
#   - Assert 403 status

from app.models import VerificationCode


def test_register_success(client):
    """POST /auth/register with a valid YorkU email returns 201."""
    resp = client.post("/auth/register", json={
        "email": "newuser@my.yorku.ca",
        "password": "securepass1",
        "name": "New User",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert "user_id" in data
    assert "message" in data


def test_register_invalid_domain(client):
    """POST /auth/register with a non-YorkU email returns 400 (validation error)."""
    resp = client.post("/auth/register", json={
        "email": "user@gmail.com",
        "password": "securepass1",
        "name": "Bad Domain",
    })
    assert resp.status_code == 422  # Pydantic validation error


def test_register_duplicate_email(client):
    """Registering twice with the same email returns 409 on the second attempt."""
    payload = {
        "email": "duplicate@my.yorku.ca",
        "password": "securepass1",
        "name": "Dup User",
    }
    resp1 = client.post("/auth/register", json=payload)
    assert resp1.status_code == 201

    resp2 = client.post("/auth/register", json=payload)
    assert resp2.status_code == 409


def test_verify_success(client, db_session):
    """Verifying with the correct code returns 200."""
    client.post("/auth/register", json={
        "email": "verify@my.yorku.ca",
        "password": "securepass1",
        "name": "Verify User",
    })
    code_row = db_session.query(VerificationCode).order_by(VerificationCode.id.desc()).first()

    resp = client.post("/auth/verify", json={
        "email": "verify@my.yorku.ca",
        "code": code_row.code,
    })
    assert resp.status_code == 200


def test_verify_wrong_code(client, db_session):
    """Verifying with an incorrect code returns 400."""
    client.post("/auth/register", json={
        "email": "wrongcode@my.yorku.ca",
        "password": "securepass1",
        "name": "Wrong Code",
    })

    resp = client.post("/auth/verify", json={
        "email": "wrongcode@my.yorku.ca",
        "code": "000000",
    })
    assert resp.status_code == 400


def test_login_success(client, db_session):
    """Login with correct credentials after verification returns 200 with token."""
    client.post("/auth/register", json={
        "email": "loginok@my.yorku.ca",
        "password": "securepass1",
        "name": "Login User",
    })
    code_row = db_session.query(VerificationCode).order_by(VerificationCode.id.desc()).first()
    client.post("/auth/verify", json={
        "email": "loginok@my.yorku.ca",
        "code": code_row.code,
    })

    resp = client.post("/auth/login", json={
        "email": "loginok@my.yorku.ca",
        "password": "securepass1",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["email"] == "loginok@my.yorku.ca"


def test_login_wrong_password(client, db_session):
    """Login with wrong password returns 401."""
    client.post("/auth/register", json={
        "email": "wrongpw@my.yorku.ca",
        "password": "securepass1",
        "name": "WrongPW User",
    })
    code_row = db_session.query(VerificationCode).order_by(VerificationCode.id.desc()).first()
    client.post("/auth/verify", json={
        "email": "wrongpw@my.yorku.ca",
        "code": code_row.code,
    })

    resp = client.post("/auth/login", json={
        "email": "wrongpw@my.yorku.ca",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401


def test_login_unverified(client):
    """Login without verifying email first returns 403."""
    client.post("/auth/register", json={
        "email": "unverified@my.yorku.ca",
        "password": "securepass1",
        "name": "Unverified User",
    })

    resp = client.post("/auth/login", json={
        "email": "unverified@my.yorku.ca",
        "password": "securepass1",
    })
    assert resp.status_code == 403

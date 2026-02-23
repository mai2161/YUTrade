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

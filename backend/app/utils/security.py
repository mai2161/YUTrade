# Assigned to: Daniel Chahine
# Phase: 1 (B1.5)
#
# TODO: Implement password hashing and JWT token utilities.
#
# Password Hashing (using passlib with bcrypt):
#
# hash_password(password: str) -> str:
#   - Use passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")
#   - Return pwd_context.hash(password)
#
# verify_password(plain_password: str, hashed_password: str) -> bool:
#   - Return pwd_context.verify(plain_password, hashed_password)
#
# JWT Token (using python-jose):
#
# create_access_token(data: dict) -> str:
#   - Copy data dict
#   - Add "exp" claim: datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#   - Encode with jose.jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
#   - Return the token string
#
# decode_access_token(token: str) -> dict | None:
#   - Try jose.jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#   - Return the payload dict on success
#   - Return None (or raise) on ExpiredSignatureError or JWTError

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from app.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create a JWT access token with an expiration claim."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Decode and validate a JWT access token. Returns payload dict or None."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (ExpiredSignatureError, JWTError):
        return None

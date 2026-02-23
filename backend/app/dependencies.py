# Assigned to: Daniel Chahine
# Phase: 1 (B1.6)
#
# TODO: Create shared FastAPI dependencies.
#
# 1. get_db() generator:
#    - Yields a SessionLocal() instance
#    - Closes the session in a finally block
#    - Usage: db: Session = Depends(get_db)
#
# 2. get_current_user(token, db) dependency:
#    - Extract token from Authorization header using OAuth2PasswordBearer(tokenUrl="/auth/login")
#    - Decode the JWT using security.decode_access_token()
#    - Extract user_id from the token payload ("sub" claim)
#    - Query the database for the user by id
#    - Raise HTTPException(401) if token is invalid or user not found
#    - Return the User ORM object
#    - Usage: current_user: User = Depends(get_current_user)

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    """Yield a database session, closing it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Decode JWT and return the authenticated User, or raise 401."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user

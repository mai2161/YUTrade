# Assigned to: Daniel Chahine
# Phase: 1 (B1.7)
#
# TODO: Implement authentication business logic.
#
# This service layer is called by routers/auth.py. It contains the core logic
# separated from HTTP concerns.
#
# register_user(db, email, password, name) -> User:
#   - Validate email domain (@my.yorku.ca or @yorku.ca)
#   - Check for existing user with same email
#   - Hash the password
#   - Create and save User(is_verified=False)
#   - Generate 6-digit random code (e.g. random.randint(100000, 999999))
#   - Create VerificationCode with expires_at = now + 15 minutes
#   - Call email_service.send_verification_email(email, code)
#   - Return the created user
#
# verify_user(db, email, code) -> bool:
#   - Look up user by email
#   - Find most recent VerificationCode where used=False and expires_at > now
#   - Compare code
#   - If match: mark code as used, set user.is_verified = True, commit, return True
#   - Otherwise: return False (or raise appropriate error)
#
# authenticate_user(db, email, password) -> User | None:
#   - Look up user by email
#   - Verify password hash
#   - Check is_verified
#   - Return user if all checks pass, None otherwise

import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.config import settings
from app.models.user import User
from app.models.verification import VerificationCode
from app.utils.security import hash_password, verify_password
from app.services.email_service import send_verification_email

ALLOWED_DOMAINS = ("@my.yorku.ca", "@yorku.ca")


def register_user(db: Session, email: str, password: str, name: str) -> User:
    """Register a new user, generate verification code, and send it."""
    # Validate email domain
    email_lower = email.lower()
    if not any(email_lower.endswith(domain) for domain in ALLOWED_DOMAINS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must be a @my.yorku.ca or @yorku.ca address",
        )

    # Check for existing user
    existing = db.query(User).filter(User.email == email_lower).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    # Create user
    user = User(
        email=email_lower,
        password_hash=hash_password(password),
        name=name,
        is_verified=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate and save verification code
    code = str(random.randint(100000, 999999))
    verification = VerificationCode(
        user_id=user.id,
        code=code,
        expires_at=datetime.utcnow() + timedelta(minutes=settings.VERIFICATION_CODE_EXPIRE_MINUTES),
    )
    db.add(verification)
    db.commit()

    # Send verification email (console or SMTP)
    send_verification_email(email_lower, code)

    return user


def verify_user(db: Session, email: str, code: str) -> bool:
    """Verify a user's email with the provided code."""
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    # Find the most recent unused, non-expired verification code
    verification = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.user_id == user.id,
            VerificationCode.used == False,
            VerificationCode.expires_at > datetime.utcnow(),
        )
        .order_by(VerificationCode.id.desc())
        .first()
    )

    if not verification or verification.code != code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code",
        )

    # Mark code as used and verify the user
    verification.used = True
    user.is_verified = True
    db.commit()

    return True


def authenticate_user(db: Session, email: str, password: str) -> User:
    """Authenticate a user by email and password. Raises on failure."""
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please verify your email first.",
        )

    return user

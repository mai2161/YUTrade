# Assigned to: Daniel Chahine
# Phase: 1 (B1.8)
#
# TODO: Implement authentication API endpoints.
#
# Create router = APIRouter()
#
# POST /register
#   - Request body: RegisterRequest (email, password, name)
#   - Validate email domain ends with @my.yorku.ca or @yorku.ca → 400 if not
#   - Check if email already exists in DB → 409 if duplicate
#   - Hash the password using security.hash_password()
#   - Create User in DB with is_verified=False
#   - Generate a 6-digit verification code, save as VerificationCode with expires_at
#   - Send verification email (or log to console in dev mode) via email_service
#   - Return 201: {"message": "Verification code sent to your email", "user_id": user.id}
#
# POST /verify
#   - Request body: VerifyRequest (email, code)
#   - Look up user by email → 400 if not found
#   - Look up most recent unused, non-expired VerificationCode for user
#   - If code matches: mark code as used, set user.is_verified = True → 200
#   - If code doesn't match or is expired → 400
#
# POST /login
#   - Request body: LoginRequest (email, password)
#   - Look up user by email → 401 if not found
#   - Verify password using security.verify_password() → 401 if wrong
#   - Check user.is_verified → 403 if not verified
#   - Create JWT access token with sub=str(user.id) using security.create_access_token()
#   - Return 200: TokenResponse {access_token, token_type: "bearer", user: UserOut}

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.auth import RegisterRequest, VerifyRequest, LoginRequest, TokenResponse
from app.schemas.user import UserOut
from app.services.auth_service import register_user, verify_user, authenticate_user
from app.utils.security import create_access_token

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user and send a verification code."""
    user = register_user(db, request.email, request.password, request.name)
    return {"message": "Verification code sent to your email", "user_id": user.id}


@router.post("/verify", status_code=status.HTTP_200_OK)
def verify(request: VerifyRequest, db: Session = Depends(get_db)):
    """Verify a user's email with the provided 6-digit code."""
    verify_user(db, request.email, request.code)
    return {"message": "Email verified successfully"}


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user and return a JWT access token."""
    user = authenticate_user(db, request.email, request.password)
    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserOut.model_validate(user),
    )

# Assigned to: Daniel Chahine
# Phase: 1 (B1.4)
#
# TODO: Define Pydantic schemas for authentication endpoints.
#
# RegisterRequest:
#   - email: EmailStr (must end with @my.yorku.ca or @yorku.ca)
#   - password: str (min length 8)
#   - name: str (min length 1)
#
# VerifyRequest:
#   - email: EmailStr
#   - code: str (exactly 6 characters)
#
# LoginRequest:
#   - email: EmailStr
#   - password: str
#
# TokenResponse:
#   - access_token: str
#   - token_type: str (always "bearer")
#   - user: UserOut (see schemas/user.py)

from pydantic import BaseModel, EmailStr, field_validator
from app.schemas.user import UserOut

ALLOWED_DOMAINS = ("@my.yorku.ca", "@yorku.ca")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

    @field_validator("email")
    @classmethod
    def validate_york_email(cls, v: str) -> str:
        if not any(v.lower().endswith(domain) for domain in ALLOWED_DOMAINS):
            raise ValueError("Email must be a @my.yorku.ca or @yorku.ca address")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if len(v.strip()) < 1:
            raise ValueError("Name must not be empty")
        return v.strip()


class VerifyRequest(BaseModel):
    email: EmailStr
    code: str

    @field_validator("code")
    @classmethod
    def validate_code_length(cls, v: str) -> str:
        if len(v) != 6:
            raise ValueError("Code must be exactly 6 characters")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

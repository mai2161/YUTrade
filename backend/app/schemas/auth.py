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

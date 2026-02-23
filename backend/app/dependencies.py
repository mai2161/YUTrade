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

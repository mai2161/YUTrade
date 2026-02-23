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

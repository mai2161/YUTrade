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

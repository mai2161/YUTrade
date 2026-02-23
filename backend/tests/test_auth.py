# Assigned to: Daniel Chahine + Mickey (Michael Byalsky)
# Phase: 1 (B1.9)
#
# TODO: Write tests for authentication endpoints.
#
# Test cases to implement:
#
# test_register_success:
#   - POST /auth/register with valid YorkU email
#   - Assert 201 status, response has "user_id" and "message"
#
# test_register_invalid_domain:
#   - POST /auth/register with non-YorkU email (e.g. "user@gmail.com")
#   - Assert 400 status
#
# test_register_duplicate_email:
#   - Register once, then register again with same email
#   - Assert 409 status on second attempt
#
# test_verify_success:
#   - Register a user, retrieve the verification code from DB
#   - POST /auth/verify with correct code
#   - Assert 200 status
#
# test_verify_wrong_code:
#   - Register a user
#   - POST /auth/verify with wrong code
#   - Assert 400 status
#
# test_login_success:
#   - Register and verify a user
#   - POST /auth/login with correct credentials
#   - Assert 200 status, response has "access_token" and "user"
#
# test_login_wrong_password:
#   - Register and verify a user
#   - POST /auth/login with wrong password
#   - Assert 401 status
#
# test_login_unverified:
#   - Register but do NOT verify
#   - POST /auth/login
#   - Assert 403 status

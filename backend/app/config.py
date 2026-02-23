# Assigned to: Mickey (Michael Byalsky)
# Phase: 1 (B1.2)
#
# TODO: Create application settings using environment variables.
#
# 1. Use python-dotenv to load .env file
# 2. Create a Settings class (can use pydantic BaseSettings or simple os.getenv):
#    - SECRET_KEY: str (used for JWT signing)
#    - DATABASE_URL: str (default: "sqlite:///./yutrade.db")
#    - EMAIL_BACKEND: str (default: "console" — logs codes to terminal instead of sending email)
#    - SMTP_HOST: str (default: "smtp.gmail.com")
#    - SMTP_PORT: int (default: 587)
#    - SMTP_USER: str (default: "")
#    - SMTP_PASSWORD: str (default: "")
#    - ACCESS_TOKEN_EXPIRE_MINUTES: int (default: 60)
#    - VERIFICATION_CODE_EXPIRE_MINUTES: int (default: 15)
# 3. Export a single `settings` instance for use across the app

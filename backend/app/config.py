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

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./yutrade.db")
    EMAIL_BACKEND: str = os.getenv("EMAIL_BACKEND", "console")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    VERIFICATION_CODE_EXPIRE_MINUTES: int = int(os.getenv("VERIFICATION_CODE_EXPIRE_MINUTES", "15"))


settings = Settings()

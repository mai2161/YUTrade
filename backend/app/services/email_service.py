# Assigned to: Daniel Chahine
# Phase: 1 (B1.7)
#
# TODO: Implement email sending for verification codes.
#
# send_verification_email(email: str, code: str) -> None:
#   - Check settings.EMAIL_BACKEND
#   - If "console" (dev mode):
#       - Print to terminal: f"[DEV] Verification code for {email}: {code}"
#       - This lets developers test without SMTP setup
#   - If "smtp" (production mode):
#       - Use aiosmtplib to send an email via settings.SMTP_HOST/PORT/USER/PASSWORD
#       - Subject: "YU Trade - Email Verification"
#       - Body: f"Your verification code is: {code}\nThis code expires in 15 minutes."
#       - From: settings.SMTP_USER
#       - To: email
#
# Note: For this course project, "console" mode is the primary mode.
# SMTP is optional/bonus functionality.

from email.message import EmailMessage
from app.config import settings


def send_verification_email(email: str, code: str) -> None:
    """Send a verification code via console log or SMTP."""
    if settings.EMAIL_BACKEND == "console":
        # Dev mode — just print the code to the terminal
        print(f"[DEV] Verification code for {email}: {code}")
    elif settings.EMAIL_BACKEND == "smtp":
        import asyncio
        import aiosmtplib

        msg = EmailMessage()
        msg["Subject"] = "YU Trade - Email Verification"
        msg["From"] = settings.SMTP_USER
        msg["To"] = email
        msg.set_content(
            f"Your YU Trade verification code is: {code}\n\nThis code expires in 15 minutes.\n\nIf you did not register for YU Trade, you can ignore this email."
        )

        try:
            asyncio.run(
                aiosmtplib.send(
                    msg,
                    hostname=settings.SMTP_HOST,
                    port=settings.SMTP_PORT,
                    username=settings.SMTP_USER,
                    password=settings.SMTP_PASSWORD,
                    start_tls=True,
                )
            )
            print(f"[SMTP] Verification email sent to {email}")
        except Exception as e:
            print(f"[SMTP ERROR] Failed to send email to {email}: {e}")
            print(f"[FALLBACK] Verification code for {email}: {code}")
    else:
        # Fallback — treat unknown backends as console
        print(f"[DEV] Verification code for {email}: {code}")

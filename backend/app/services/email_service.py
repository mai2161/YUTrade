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

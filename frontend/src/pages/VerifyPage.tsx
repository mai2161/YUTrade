// Assigned to: Mai Komar
// Phase: 1 (F1.5)
//
// TODO: Email verification page.
//
// User arrives here after registration with email in URL query param.
//
// Form fields:
//   - Email (pre-filled from query param, read-only or editable)
//   - Verification Code (text input, 6 digits)
//
// Behavior:
//   1. Read email from URL: new URLSearchParams(location.search).get("email")
//   2. On submit, call api/auth.ts verify({ email, code })
//   3. On success: show success message, redirect to /login after 2 seconds
//   4. On error: show "Invalid or expired verification code"
//   5. Show loading spinner while request is in flight
//
// Styling: Simple centered form with YU branding
// Note: In dev mode, the code is logged to the backend console — tell user to check terminal

// Assigned to: Mai Komar
// Phase: 1 (F1.5)
//
// TODO: Registration page for new users.
//
// Form fields:
//   - Name (text input, required)
//   - Email (email input, required — must be @my.yorku.ca or @yorku.ca)
//   - Password (password input, required, min 8 characters)
//   - Confirm Password (must match)
//
// Behavior:
//   1. Validate email domain on client side before submitting
//      (show error if not a YorkU email)
//   2. Validate passwords match
//   3. On submit, call api/auth.ts register()
//   4. On success: redirect to /verify?email={email} so user can enter code
//   5. On error (409 duplicate): show "Email already registered"
//   6. On error (400 bad domain): show "Must use a YorkU email"
//   7. Show loading spinner while request is in flight
//
// Styling: Use YU branding (red #E31837 for buttons, clean form layout)
// Link: "Already have an account? Log in" -> /login

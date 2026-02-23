// Assigned to: Mai Komar
// Phase: 1 (F1.5)
//
// TODO: Login page.
//
// Form fields:
//   - Email (email input, required)
//   - Password (password input, required)
//
// Behavior:
//   1. On submit, call api/auth.ts login({ email, password })
//   2. On success:
//      - Call auth context's login(token, user) to store JWT and user
//      - Redirect to / (BrowsePage)
//   3. On 401 error: show "Invalid email or password"
//   4. On 403 error: show "Please verify your email first" with link to /verify
//   5. Show loading spinner while request is in flight
//
// Styling: Use YU branding (red #E31837 for submit button)
// Links:
//   - "Don't have an account? Register" -> /register
//   - "Need to verify your email?" -> /verify

// Assigned to: Harnaindeep Kaur
// Phase: 1 (F1.4)
//
// TODO: Client-side validation helpers.
//
// isYorkUEmail(email: string): boolean
//   - Return true if email ends with "@my.yorku.ca" or "@yorku.ca"
//   - Case-insensitive check
//   - Used on RegisterPage to validate before submitting
//
// isValidPassword(password: string): { valid: boolean; message: string }
//   - Min 8 characters
//   - Return { valid: false, message: "Password must be at least 8 characters" } if too short
//   - Return { valid: true, message: "" } if OK
//
// isValidPrice(price: string | number): boolean
//   - Must be a number > 0
//   - Used on CreateListingPage
//
// formatPrice(price: number): string
//   - Return price formatted as "$XX.XX"
//   - e.g. formatPrice(25) -> "$25.00"
//
// formatDate(isoString: string): string
//   - Convert ISO datetime string to human-readable format
//   - e.g. "Feb 22, 2026" or "2 hours ago" (relative time)
//   - Used across ListingCard, ListingDetailPage, MessageThread

// Assigned to: Mai Komar
// Phase: 2 (F2.5)
//
// TODO: Create new listing page (protected — requires authentication).
//
// Form fields:
//   - Title (text input, required, max 200 chars)
//   - Description (textarea, optional)
//   - Price (number input, required, min 0.01)
//   - Category (dropdown select, optional)
//       Options: "Textbooks", "Electronics", "Furniture", "Clothing", "Other"
//   - Images (file input, multiple, optional — uses ImageUpload component)
//
// Behavior:
//   1. Build a FormData object on submit:
//      - Append title, description, price, category as form fields
//      - Append each selected image file as "images"
//   2. Call api/listings.ts createListing(formData)
//   3. On success: redirect to /listings/{newListing.id}
//   4. On error: show validation errors
//   5. Show loading spinner while submitting
//
// Validation:
//   - Title is required
//   - Price must be a positive number
//   - Images should be image files (jpg, png, gif, webp)
//   - Max file size: 5MB per image (client-side check)

// Assigned to: Mai Komar
// Phase: 2 (F2.4)
//
// TODO: Single listing detail page.
//
// Layout:
//   - Image gallery/carousel (show all listing images, first image is primary)
//   - Listing details: title, price (formatted as $XX.XX), category badge, status
//   - Description section
//   - Seller info: name, email
//   - "Contact Seller" button (visible if logged in and not the seller)
//   - Phase 3 (F3.3): Message thread section below listing details
//
// Behavior:
//   1. Read listing ID from URL params: useParams<{ id: string }>()
//   2. On mount, call api/listings.ts getListing(id)
//   3. Display listing data
//   4. Image display: show images from listing.images array
//      - Image URLs: `${API_URL}/${image.file_path}`
//      - Show placeholder if no images
//   5. "Contact Seller" button:
//      - If not logged in: redirect to /login
//      - If logged in: scroll to / show message thread (Phase 3)
//   6. Handle 404: show "Listing not found" page
//   7. Show loading spinner while fetching
//
// Phase 3 additions:
//   - MessageThread component for sending/viewing messages about this listing
//   - Only visible to authenticated users

// Assigned to: Harnaindeep Kaur
// Phase: 2 (F2.6)
//
// TODO: Page showing the current user's own listings (protected).
//
// Layout:
//   - Page title: "My Listings"
//   - List/grid of the user's listings (all statuses: active, sold, removed)
//   - Each listing shows: title, price, status badge, created date
//   - Status toggle: dropdown or buttons to change status (active/sold/removed)
//   - "Create New Listing" button at top -> /create
//   - Empty state: "You haven't created any listings yet"
//
// Behavior:
//   1. On mount, call api/listings.ts getListings() filtered by current user
//      (Note: may need a query param like seller_id, or filter client-side,
//       or add a /listings/mine endpoint — coordinate with Lakshan)
//   2. Display listings with their current status
//   3. Status change: call api/listings.ts updateListing(id, { status: newStatus })
//      - On success: update the listing in local state
//      - Show confirmation before marking as "removed"
//   4. Clicking a listing title navigates to /listings/{id}
//   5. Show loading spinner while fetching

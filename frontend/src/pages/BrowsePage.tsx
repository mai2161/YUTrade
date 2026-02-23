// Assigned to: Harnaindeep Kaur
// Phase: 2 (F2.3)
//
// TODO: Main browse/home page showing all active listings.
//
// Layout:
//   - SearchBar component at top (Phase 3: F3.6)
//   - Grid of ListingCard components (responsive: 1 col mobile, 2 col tablet, 3-4 col desktop)
//   - Pagination controls at bottom (Previous / Next / page numbers)
//   - Empty state: "No listings found" message when no results
//
// Behavior:
//   1. On mount, call api/listings.ts getListings({ status: "active", page: 1, limit: 20 })
//   2. Display listings in a grid using ListingCard component
//   3. Clicking a card navigates to /listings/{id}
//   4. Support pagination: update page param and re-fetch
//   5. Phase 3: Integrate SearchBar for search text, category filter, price range
//   6. Show loading spinner while fetching
//   7. Handle errors with user-friendly message
//
// State:
//   - listings: Listing[]
//   - total: number
//   - page: number
//   - loading: boolean
//   - error: string | null
//   - searchParams: { search?, category?, min_price?, max_price? } (Phase 3)

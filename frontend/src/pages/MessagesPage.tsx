// Assigned to: Harnaindeep Kaur
// Phase: 3 (F3.4)
//
// TODO: Page showing all message conversations (protected).
//
// Layout:
//   - Page title: "Messages"
//   - List of conversation threads, grouped by listing
//   - Each thread shows:
//       - Listing title and thumbnail
//       - Other person's name
//       - Last message preview (truncated)
//       - Timestamp of last message
//   - Clicking a thread navigates to /listings/{id} (with message section visible)
//   - Empty state: "No messages yet"
//
// Behavior:
//   1. On mount, fetch all listings where the user has sent or received messages
//      (This may require a dedicated endpoint or fetching from multiple listing threads)
//   2. Display threads sorted by most recent message first
//   3. Show loading spinner while fetching
//   4. Handle errors gracefully
//
// Note: The exact API approach for getting "all threads" may need coordination
// with Raj's backend implementation. Options:
//   a) A new GET /messages endpoint that returns all threads for the current user
//   b) Client-side aggregation from multiple listing message endpoints
//   Discuss with Raj to decide the best approach.

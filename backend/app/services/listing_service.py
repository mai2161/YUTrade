# Assigned to: Lakshan Kandeepan
# Phase: 2 (B2.3)
#
# TODO: Implement listing business logic.
#
# create_listing(db, seller_id, title, description, price, category, images) -> Listing:
#   - Create Listing record in DB
#   - For each uploaded image file:
#       - Generate a UUID-based filename to avoid collisions (e.g. f"{uuid4()}.{ext}")
#       - Save file to uploads/ directory
#       - Create Image record with file_path and position (index)
#   - Commit and return the listing with relationships loaded
#
# get_listings(db, search, category, status, page, limit) -> (List[Listing], total):
#   - Start with query on Listing
#   - Filter by status (default "active")
#   - If search: filter where title ILIKE %search% OR description ILIKE %search%
#   - If category: filter where category == category
#   - Phase 3 (B3.5): Add min_price/max_price filtering
#   - Count total matching records
#   - Apply offset = (page - 1) * limit and limit
#   - Return (listings, total_count)
#
# get_listing_by_id(db, listing_id) -> Listing | None:
#   - Query listing by ID with joinedload on images and seller
#   - Return listing or None
#
# update_listing(db, listing_id, seller_id, update_data) -> Listing:
#   - Fetch listing, verify seller_id matches
#   - Update only provided fields (title, description, price, status)
#   - Set updated_at to now
#   - Commit and return updated listing

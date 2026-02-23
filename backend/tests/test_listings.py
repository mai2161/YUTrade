# Assigned to: Lakshan Kandeepan
# Phase: 2 (B2.6)
#
# TODO: Write tests for listing endpoints.
#
# Test cases to implement:
#
# test_create_listing_success:
#   - POST /listings with auth headers, valid form data (title, price, etc.)
#   - Assert 201 status, response has listing id, title, seller_id
#
# test_create_listing_unauthorized:
#   - POST /listings without auth headers
#   - Assert 401 status
#
# test_get_listings:
#   - Create a few listings
#   - GET /listings
#   - Assert 200 status, response has "listings" array and "total"
#
# test_get_listings_search:
#   - Create listings with different titles
#   - GET /listings?search=keyword
#   - Assert only matching listings returned
#
# test_get_listings_category_filter:
#   - Create listings with different categories
#   - GET /listings?category=Textbooks
#   - Assert only matching listings returned
#
# test_get_listing_by_id:
#   - Create a listing
#   - GET /listings/{id}
#   - Assert 200, response has full listing with images and seller
#
# test_get_listing_not_found:
#   - GET /listings/99999
#   - Assert 404
#
# test_update_listing_owner:
#   - Create listing, then PATCH /listings/{id} with owner's auth
#   - Assert 200, fields are updated
#
# test_update_listing_not_owner:
#   - Create listing as user A, try PATCH with user B's auth
#   - Assert 403
#
# test_create_listing_with_images:
#   - POST /listings with image files attached
#   - Assert images appear in response, files exist on disk

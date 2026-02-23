# Assigned to: Raj (Rajendra Brahmbhatt)
# Phase: 3 (B3.6)
#
# TODO: Write tests for messaging endpoints.
#
# Test cases to implement:
#
# test_send_message_to_seller:
#   - User A creates a listing
#   - User B sends a message via POST /listings/{id}/messages
#   - Assert 201, message has correct sender_id, receiver_id (seller), listing_id
#
# test_seller_reply:
#   - User B messages User A's listing
#   - User A replies via POST /listings/{id}/messages
#   - Assert 201, receiver is User B
#
# test_get_messages:
#   - Exchange a few messages between users on a listing
#   - GET /listings/{id}/messages as either participant
#   - Assert 200, messages returned in chronological order
#
# test_send_message_unauthorized:
#   - POST /listings/{id}/messages without auth
#   - Assert 401
#
# test_get_messages_non_participant:
#   - User C (not involved) tries GET /listings/{id}/messages
#   - Assert 403 or empty list (depending on implementation choice)
#
# test_send_message_listing_not_found:
#   - POST /listings/99999/messages
#   - Assert 404
#
# test_cannot_message_self:
#   - Seller tries to start a thread on their own listing (no prior buyer message)
#   - Assert 400 (no receiver to determine)

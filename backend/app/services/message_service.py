# Assigned to: Raj (Rajendra Brahmbhatt)
# Phase: 3 (B3.3)
#
# TODO: Implement messaging business logic.
#
# send_message(db, listing_id, sender_id, content) -> Message:
#   - Fetch the listing → raise error if not found
#   - Determine receiver_id:
#       - If sender is NOT the seller → receiver = listing.seller_id
#       - If sender IS the seller → receiver = the other user in the existing thread
#         (query messages for this listing to find the other participant)
#   - Validate sender_id != receiver_id (can't message yourself)
#   - Create Message record with listing_id, sender_id, receiver_id, content
#   - Commit and return the message with sender relationship loaded
#
# get_messages(db, listing_id, user_id) -> List[Message]:
#   - Query all messages for this listing where user_id is either sender or receiver
#   - Order by created_at ascending (oldest first)
#   - Return list of messages with sender relationship loaded
#
# get_user_threads(db, user_id) -> List[dict]:
#   - Find all unique (listing_id, other_user_id) pairs where user_id participated
#   - For each thread, get the latest message and unread count
#   - Return list of thread summaries ordered by most recent message
#   - This is used by the frontend MessagesPage to show all conversations

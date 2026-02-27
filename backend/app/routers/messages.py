# Assigned to: Raj (Rajendra Brahmbhatt)
# Phase: 3 (B3.4)
#
# TODO: Implement messaging API endpoints.
#
# Create router = APIRouter()
#
# Note: These routes are nested under /listings/{listing_id}/messages
# Include this router in main.py with prefix="/listings/{listing_id}/messages"
# OR include within the listings router.
#
# POST /
#   - Auth: Required (Depends(get_current_user))
#   - Path param: listing_id (int)
#   - Request body: MessageCreate {content: str}
#   - Logic:
#       - Verify listing exists → 404 if not
#       - Sender is current_user
#       - Receiver is the listing's seller (if sender != seller)
#       - If sender IS the seller, receiver should be determined from the existing
#         message thread (the other participant who initiated the conversation)
#       - A buyer cannot message themselves (sender_id != receiver_id)
#       - Call message_service.send_message()
#   - Return 201: MessageOut
#
# GET /
#   - Auth: Required (must be seller or a participant in the thread)
#   - Path param: listing_id (int)
#   - Logic:
#       - Get all messages for this listing where current_user is sender or receiver
#       - Order by created_at ascending
#       - Call message_service.get_messages()
#   - Return 200: {messages: List[MessageOut]}

from fastapi import APIRouter, Depends, status

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
def message_health():
    return {"message": "Hello, World! From messages.py"}
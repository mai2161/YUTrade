# Assigned to: Raj (Rajendra Brahmbhatt)
# Phase: 3 (B3.2)
#
# TODO: Define Pydantic schemas for messaging endpoints.
#
# MessageCreate (for POST /listings/{id}/messages):
#   - content: str (min length 1)
#
# SenderOut (minimal user info on a message):
#   - id: int
#   - name: str
#   class Config: from_attributes = True
#
# MessageOut (single message response):
#   - id: int
#   - listing_id: int
#   - sender_id: int
#   - receiver_id: int
#   - sender: SenderOut
#   - content: str
#   - created_at: datetime
#   class Config: from_attributes = True

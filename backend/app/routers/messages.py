# Assigned to: Raj (Rajendra Brahmbhatt)
# Phase: 3 (B3.4)
#
# Messaging API endpoints.
# These routes are nested under /listings/{listing_id}/messages

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.message import MessageCreate, MessageOut
from app.services.message_service import send_message, get_messages

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MessageOut)
def create_message(
    listing_id: int,
    body: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Send a message on a listing."""
    message = send_message(db, listing_id, current_user.id, body.content)
    return message


@router.get("/", status_code=status.HTTP_200_OK)
def list_messages(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all messages for a listing where current user is a participant."""
    messages = get_messages(db, listing_id, current_user.id)
    return {"messages": [MessageOut.model_validate(m) for m in messages]}

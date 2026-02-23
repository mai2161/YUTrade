# Assigned to: Raj (Rajendra Brahmbhatt)
# Phase: 3 (B3.3)

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func, desc
from fastapi import HTTPException, status

from app.models.message import Message
from app.models.listing import Listing


def send_message(db: Session, listing_id: int, sender_id: int, content: str) -> Message:
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found",
        )

    if sender_id != listing.seller_id:
        receiver_id = listing.seller_id
    else:
        existing = (
            db.query(Message)
            .filter(
                Message.listing_id == listing_id,
                or_(
                    Message.sender_id == sender_id,
                    Message.receiver_id == sender_id,
                ),
            )
            .order_by(Message.created_at.desc())
            .first()
        )
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No existing conversation — seller cannot initiate a message thread",
            )
        receiver_id = (
            existing.receiver_id
            if existing.sender_id == sender_id
            else existing.sender_id
        )

    if sender_id == receiver_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send a message to yourself",
        )

    message = Message(
        listing_id=listing_id,
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    db.query(Message).options(joinedload(Message.sender)).filter(
        Message.id == message.id
    ).first()

    return message


def get_messages(db: Session, listing_id: int, user_id: int) -> list[Message]:
    messages = (
        db.query(Message)
        .options(joinedload(Message.sender))
        .filter(
            Message.listing_id == listing_id,
            or_(
                Message.sender_id == user_id,
                Message.receiver_id == user_id,
            ),
        )
        .order_by(Message.created_at.asc())
        .all()
    )
    return messages


def get_user_threads(db: Session, user_id: int) -> list[dict]:
    user_messages = (
        db.query(Message)
        .filter(
            or_(
                Message.sender_id == user_id,
                Message.receiver_id == user_id,
            )
        )
        .all()
    )

    threads: dict[tuple[int, int], list[Message]] = {}
    for msg in user_messages:
        other_user_id = (
            msg.receiver_id if msg.sender_id == user_id else msg.sender_id
        )
        key = (msg.listing_id, other_user_id)
        threads.setdefault(key, []).append(msg)

    result = []
    for (listing_id, other_user_id), messages in threads.items():
        latest = max(messages, key=lambda m: m.created_at)
        listing = db.query(Listing).filter(Listing.id == listing_id).first()

        result.append(
            {
                "listing_id": listing_id,
                "listing_title": listing.title if listing else "Deleted listing",
                "other_user_id": other_user_id,
                "last_message": latest.content,
                "last_message_at": latest.created_at,
                "message_count": len(messages),
            }
        )

    result.sort(key=lambda t: t["last_message_at"], reverse=True)
    return result

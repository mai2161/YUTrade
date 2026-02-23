# Assigned to: Raj (Rajendra Brahmbhatt)
# Phase: 3 (B3.2)

from datetime import datetime
from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1)


class SenderOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MessageOut(BaseModel):
    id: int
    listing_id: int
    sender_id: int
    receiver_id: int
    sender: SenderOut
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

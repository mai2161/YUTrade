# Assigned to: Mickey (Michael Byalsky)
# Phase: 3 (B3.1)
#
# TODO: Define the Message ORM model.
#
# Table name: "messages"
# Columns:
#   - id: Integer, primary_key, autoincrement
#   - listing_id: Integer, ForeignKey("listings.id"), nullable=False, index=True
#   - sender_id: Integer, ForeignKey("users.id"), nullable=False, index=True
#   - receiver_id: Integer, ForeignKey("users.id"), nullable=False, index=True
#   - content: Text, nullable=False
#   - created_at: DateTime, nullable=False, default=datetime.utcnow
#
# Relationships:
#   - listing: relationship("Listing", back_populates="messages")
#   - sender: relationship("User", foreign_keys=[sender_id])
#   - receiver: relationship("User", foreign_keys=[receiver_id])

from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    listing = relationship("Listing", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

# Assigned to: Mickey (Michael Byalsky)
# Phase: 1 (B1.3)
#
# TODO: Define the User ORM model.
#
# Table name: "users"
# Columns:
#   - id: Integer, primary_key, autoincrement
#   - email: String(255), unique, nullable=False
#       Must be @my.yorku.ca or @yorku.ca (validated at registration, not DB level)
#   - password_hash: String(255), nullable=False (bcrypt hash)
#   - name: String(100), nullable=False
#   - is_verified: Boolean, nullable=False, default=False
#   - created_at: DateTime, nullable=False, default=datetime.utcnow
#
# Relationships:
#   - listings: relationship("Listing", back_populates="seller")
#   - sent_messages: relationship("Message", foreign_keys="Message.sender_id")
#   - received_messages: relationship("Message", foreign_keys="Message.receiver_id")

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    listings = relationship("Listing", back_populates="seller")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id")

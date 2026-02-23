# Assigned to: Mickey (Michael Byalsky)
# Phase: 2 (B2.1)
#
# TODO: Define the Listing ORM model.
#
# Table name: "listings"
# Columns:
#   - id: Integer, primary_key, autoincrement
#   - seller_id: Integer, ForeignKey("users.id"), nullable=False, index=True
#   - title: String(200), nullable=False
#   - description: Text, nullable=True
#   - price: Numeric(10, 2), nullable=False
#   - category: String(50), nullable=True
#       Example values: "Textbooks", "Electronics", "Furniture", "Clothing", "Other"
#   - status: String(20), nullable=False, default="active", index=True
#       Possible values: "active", "sold", "removed"
#   - created_at: DateTime, nullable=False, default=datetime.utcnow
#   - updated_at: DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
#
# Relationships:
#   - seller: relationship("User", back_populates="listings")
#   - images: relationship("Image", back_populates="listing", cascade="all, delete-orphan")
#   - messages: relationship("Message", back_populates="listing")

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="active", index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    seller = relationship("User", back_populates="listings")
    images = relationship("Image", back_populates="listing", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="listing")

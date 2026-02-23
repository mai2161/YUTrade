# Assigned to: Mickey (Michael Byalsky)
# Phase: 2 (B2.1)
#
# TODO: Define the Image ORM model.
#
# Table name: "images"
# Columns:
#   - id: Integer, primary_key, autoincrement
#   - listing_id: Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False
#   - file_path: String(500), nullable=False
#       Stores relative path under uploads/, e.g. "uploads/abc123-uuid.jpg"
#   - position: Integer, nullable=False, default=0
#       Used to order images (0 = primary/first image)
#
# Relationships:
#   - listing: relationship("Listing", back_populates="images")

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(500), nullable=False)
    position = Column(Integer, nullable=False, default=0)

    listing = relationship("Listing", back_populates="images")

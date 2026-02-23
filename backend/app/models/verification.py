# Assigned to: Mickey (Michael Byalsky)
# Phase: 1 (B1.3)
#
# TODO: Define the VerificationCode ORM model.
#
# Table name: "verification_codes"
# Columns:
#   - id: Integer, primary_key, autoincrement
#   - user_id: Integer, ForeignKey("users.id"), nullable=False
#   - code: String(6), nullable=False (random 6-digit string, e.g. "482917")
#   - expires_at: DateTime, nullable=False (set to created_at + 15 minutes)
#   - used: Boolean, nullable=False, default=False
#
# Relationships:
#   - user: relationship("User")

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    code = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, nullable=False, default=False)

    user = relationship("User")

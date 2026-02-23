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

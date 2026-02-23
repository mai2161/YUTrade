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

# Assigned to: Lakshan Kandeepan
# Phase: 2 (B2.3)
#
# TODO: Implement listing business logic.
#
# create_listing(db, seller_id, title, description, price, category, images) -> Listing:
#   - Create Listing record in DB
#   - For each uploaded image file:
#       - Generate a UUID-based filename to avoid collisions (e.g. f"{uuid4()}.{ext}")
#       - Save file to uploads/ directory
#       - Create Image record with file_path and position (index)
#   - Commit and return the listing with relationships loaded
#
# get_listings(db, search, category, status, page, limit) -> (List[Listing], total):
#   - Start with query on Listing
#   - Filter by status (default "active")
#   - If search: filter where title ILIKE %search% OR description ILIKE %search%
#   - If category: filter where category == category
#   - Phase 3 (B3.5): Add min_price/max_price filtering
#   - Count total matching records
#   - Apply offset = (page - 1) * limit and limit
#   - Return (listings, total_count)
#
# get_listing_by_id(db, listing_id) -> Listing | None:
#   - Query listing by ID with joinedload on images and seller
#   - Return listing or None
#
# update_listing(db, listing_id, seller_id, update_data) -> Listing:
#   - Fetch listing, verify seller_id matches
#   - Update only provided fields (title, description, price, status)
#   - Set updated_at to now
#   - Commit and return updated listing

import os
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.image import Image
from app.models.listing import Listing


# TODO complete:
# - Create Listing record in DB
# - Save uploaded images under uploads/ using UUID filenames
# - Create Image DB rows with file_path + position
# - Commit and return listing with relationships loaded
def create_listing(
    db: Session,
    seller_id: int,
    title: str,
    description: Optional[str],
    price: float,
    category: Optional[str],
    images,
) -> Listing:
    listing = Listing(
        seller_id=seller_id,
        title=title,
        description=description,
        price=price,
        category=category,
    )

    db.add(listing)
    db.flush()  # Get listing.id before creating Image rows

    for index, image in enumerate(images):
        ext = ""
        if image.filename and "." in image.filename:
            ext = image.filename.rsplit(".", 1)[1]

        filename = f"{uuid4()}.{ext}" if ext else str(uuid4())
        file_path = os.path.join("uploads", filename)

        with open(file_path, "wb") as file_object:
            file_object.write(image.file.read())

        image_record = Image(
            listing_id=listing.id,
            file_path=file_path,
            position=index,
        )
        db.add(image_record)

    db.commit()

    # Return the listing with seller + images loaded
    return get_listing_by_id(db, listing.id)


# TODO complete:
# - Start with query on Listing
# - Filter by status
# - Apply search on title OR description
# - Apply category filter
# - Count total
# - Apply offset + limit
# - Return (listings, total)
def get_listings(
    db: Session,
    search: Optional[str],
    category: Optional[str],
    status: str,
    page: int,
    limit: int,
):
    query = db.query(Listing).options(
        joinedload(Listing.images),
        joinedload(Listing.seller),
    )

    query = query.filter(Listing.status == status)

    if search:
        query = query.filter(
            or_(
                Listing.title.ilike(f"%{search}%"),
                Listing.description.ilike(f"%{search}%"),
            )
        )

    if category:
        query = query.filter(Listing.category == category)

    total = query.count()

    offset = (page - 1) * limit
    listings = query.offset(offset).limit(limit).all()

    return listings, total


# TODO complete:
# - Query listing by ID
# - Eager-load images and seller
# - Return listing or None
def get_listing_by_id(db: Session, listing_id: int) -> Optional[Listing]:
    return (
        db.query(Listing)
        .options(
            joinedload(Listing.images),
            joinedload(Listing.seller),
        )
        .filter(Listing.id == listing_id)
        .first()
    )


# TODO complete:
# - Fetch listing
# - Verify seller_id matches
# - Update only provided fields
# - Set updated_at to now
# - Commit and return updated listing
def update_listing(
    db: Session,
    listing_id: int,
    seller_id: int,
    update_data,
):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()

    if not listing:
        return None

    if listing.seller_id != seller_id:
        raise PermissionError("Only the listing owner can update this listing")

    if update_data.title is not None:
        listing.title = update_data.title

    if update_data.description is not None:
        listing.description = update_data.description

    if update_data.price is not None:
        listing.price = update_data.price

    if update_data.status is not None:
        listing.status = update_data.status

    listing.updated_at = datetime.utcnow()

    db.commit()

    return get_listing_by_id(db, listing.id)
# Assigned to: Lakshan Kandeepan
# Phase: 2 (B2.5)
#
# TODO: Implement listings API endpoints.
#
# Create router = APIRouter()
#
# GET /
#   - Query params: search (str), category (str), status (str, default="active"),
#     page (int, default=1), limit (int, default=20)
#   - Auth: Optional (public endpoint)
#   - Call listing_service.get_listings() with filters
#   - Return 200: PaginatedListings {listings[], total, page, limit}
#   - Phase 3 (B3.5): Add min_price, max_price query params for filtering
#
# POST /
#   - Auth: Required (Depends(get_current_user))
#   - Accept multipart/form-data:
#       - title: str = Form(...)
#       - description: Optional[str] = Form(None)
#       - price: float = Form(...)
#       - category: Optional[str] = Form(None)
#       - images: List[UploadFile] = File(default=[])
#   - Call listing_service.create_listing() which:
#       - Creates Listing in DB
#       - Saves each image to uploads/ with a UUID filename
#       - Creates Image records in DB
#   - Return 201: ListingOut
#
# GET /{listing_id}
#   - Auth: Optional
#   - Fetch listing by ID with eager-loaded images and seller
#   - Return 404 if not found
#   - Return 200: ListingOut
#
# PATCH /{listing_id}
#   - Auth: Required (must be the listing owner)
#   - Request body: ListingUpdate (JSON)
#   - Only the listing's seller can update it → 403 if not owner
#   - Update only the provided fields
#   - Return 200: ListingOut

from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.listing import ListingOut, ListingUpdate, PaginatedListings
from app.services import listing_service

# TODO complete: created router = APIRouter()
router = APIRouter()


# TODO complete:
# - GET /
# - public endpoint
# - accepts search, category, status, page, limit
# - calls listing_service.get_listings()
# - returns PaginatedListings {listings, total, page, limit}
@router.get("/", response_model=PaginatedListings)
def get_listings(
    search: Optional[str] = None,
    category: Optional[str] = None,
    status: str = "active",
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    listings, total = listing_service.get_listings(
        db=db,
        search=search,
        category=category,
        status=status,
        page=page,
        limit=limit,
    )
    return {
        "listings": listings,
        "total": total,
        "page": page,
        "limit": limit,
    }


# TODO complete:
# - POST /
# - auth required with Depends(get_current_user)
# - accepts multipart/form-data
# - calls listing_service.create_listing()
# - returns 201 ListingOut
@router.post("/", response_model=ListingOut, status_code=status.HTTP_201_CREATED)
def create_listing(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    category: Optional[str] = Form(None),
    images: List[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    listing = listing_service.create_listing(
        db=db,
        seller_id=current_user.id,
        title=title,
        description=description,
        price=price,
        category=category,
        images=images,
    )
    return listing


# TODO complete:
# - GET /{listing_id}
# - public endpoint
# - fetches listing by ID
# - returns 404 if not found
# - returns 200 ListingOut
@router.get("/{listing_id}", response_model=ListingOut)
def get_listing_by_id(
    listing_id: int,
    db: Session = Depends(get_db),
):
    listing = listing_service.get_listing_by_id(db=db, listing_id=listing_id)

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    return listing


# TODO complete:
# - PATCH /{listing_id}
# - auth required
# - accepts ListingUpdate JSON body
# - only owner can update (403 if not owner)
# - updates only provided fields
# - returns 200 ListingOut
@router.patch("/{listing_id}", response_model=ListingOut)
def update_listing(
    listing_id: int,
    update_data: ListingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        listing = listing_service.update_listing(
            db=db,
            listing_id=listing_id,
            seller_id=current_user.id,
            update_data=update_data,
        )
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorized to update this listing")

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    return listing

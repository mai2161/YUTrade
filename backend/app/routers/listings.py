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

from fastapi import APIRouter, Depends, status
from app.routers.messages import router as messages_router

router = APIRouter()

router.include_router(
    messages_router,
    prefix="/{listing_id}/messages",
    tags=["Messages"],
)

@router.get("/health", status_code=status.HTTP_200_OK)
def listing_health():
    return {"message": "Hello, World! From listings.py"}
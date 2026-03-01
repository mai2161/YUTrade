# Assigned to: Lakshan Kandeepan
# Phase: 2 (B2.2)
#
# TODO: Define Pydantic schemas for listing endpoints.
#
# ListingCreate (used for POST /listings — note: actual endpoint uses Form fields, not JSON,
#   because images are uploaded as multipart. This schema documents the expected fields):
#   - title: str (max 200 chars)
#   - description: Optional[str]
#   - price: float (must be > 0)
#   - category: Optional[str]
#
# ImageOut:
#   - id: int
#   - file_path: str
#   - position: int
#   class Config: from_attributes = True
#
# SellerOut (minimal user info shown on listing):
#   - id: int
#   - name: str
#   - email: str
#   class Config: from_attributes = True
#
# ListingOut (full listing response):
#   - id: int
#   - seller_id: int
#   - seller: SellerOut
#   - title: str
#   - description: Optional[str]
#   - price: float
#   - category: Optional[str]
#   - status: str
#   - images: List[ImageOut]
#   - created_at: datetime
#   - updated_at: datetime
#   class Config: from_attributes = True
#
# ListingUpdate (for PATCH /listings/{id}):
#   - title: Optional[str]
#   - description: Optional[str]
#   - price: Optional[float]
#   - status: Optional[str] (must be one of "active", "sold", "removed")
#
# PaginatedListings (for GET /listings):
#   - listings: List[ListingOut]
#   - total: int
#   - page: int
#   - limit: int

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ListingCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: Optional[str] = None


class ImageOut(BaseModel):
    id: int
    file_path: str
    position: int

    class Config:
        from_attributes = True


class SellerOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class ListingOut(BaseModel):
    id: int
    seller_id: int
    seller: SellerOut
    title: str
    description: Optional[str]
    price: float
    category: Optional[str]
    status: str
    images: List[ImageOut]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    status: Optional[Literal["active", "sold", "removed"]] = None


class PaginatedListings(BaseModel):
    listings: List[ListingOut]
    total: int
    page: int
    limit: int

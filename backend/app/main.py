# Assigned to: Mickey (Michael Byalsky)
# Phase: 1 (B1.1)
#
# TODO: Create the FastAPI application entry point.
#
# 1. Import FastAPI, CORSMiddleware, StaticFiles
# 2. Create the FastAPI app instance with title="YU Trade API"
# 3. Configure CORS middleware:
#    - allow_origins: ["http://localhost:3000"] (React dev server)
#    - allow_credentials: True
#    - allow_methods: ["*"]
#    - allow_headers: ["*"]
# 4. Mount static files: app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# 5. Include routers with prefixes:
#    - auth_router with prefix="/auth" and tags=["Auth"]
#    - listings_router with prefix="/listings" and tags=["Listings"]
#    - messages_router (nested under listings, see routers/messages.py)
# 6. Add a lifespan or startup event that calls Base.metadata.create_all(bind=engine)
#    to auto-create tables on first run
# 7. Add a root endpoint GET "/" returning {"message": "YU Trade API"}

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.models import User, VerificationCode, Listing, Image, Message  # noqa: F401 — register models
from app.routers.auth import router as auth_router
from app.routers.listings import router as listings_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="YU Trade API", lifespan=lifespan)

# CORS middleware for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads directory exists
os.makedirs("uploads", exist_ok=True)

# Mount static files for uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(listings_router, prefix="/listings", tags=["Listings"])


@app.get("/")
def root():
    return {"message": "YU Trade API"}

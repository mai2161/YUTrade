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

from fastapi import FastAPI

# Database
from app.database.database import Base, engine

# Import models so SQLAlchemy creates the tables
from app.models import models

# Routers
from app.api.document_routes import router as document_router
from app.api.compare_routes import router as compare_router
from app.api.search_routes import router as search_router

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="AffineSurge AI Engineering Assignment",
    version="1.0",
    description="API for document versioning, comparison, and search"
)

# Register routers
app.include_router(document_router)
app.include_router(compare_router)
app.include_router(search_router)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "AffineSurge AI Engineering Assignment API is running!"
    }
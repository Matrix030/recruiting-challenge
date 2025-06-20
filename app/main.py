"""Main application module for the Validia Face Recognition API.

This module initializes the FastAPI application, includes routers,
and handles startup events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import API_V1_STR, PROJECT_NAME
from app.core.database import create_db_and_tables
from app.routers import profiles

# Initialize FastAPI app
app = FastAPI(
    title=PROJECT_NAME,
    openapi_url=f"{API_V1_STR}/openapi.json",
    docs_url="/docs",
    description="""
    Face Recognition API for Validia's recruiting challenge.
    
    Features:
    * Create face profiles with feature analysis
    * Store and retrieve face embeddings
    * Verify faces against stored profiles
    
    All face analysis is performed using InsightFace with the buffalo_l model.
    """,
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    profiles.router,
    prefix=API_V1_STR,
    tags=["profiles"]
)

@app.on_event("startup")
def on_startup() -> None:
    """Initialize database on startup."""
    create_db_and_tables() 
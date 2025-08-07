"""
Backend API server for the Candidate Recommendation application.

This module sets up the FastAPI application with:
- CORS middleware configuration for frontend communication
- Route handlers for file upload and health checks
- Environment variable configuration
- Service initialization
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from backend.routes import health_router, upload_router
from backend.services import file_service, similarity_service

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Candidate Recommendation API",
    description="API for processing resumes and matching candidates to job descriptions",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, tags=["Health"])
app.include_router(upload_router, prefix="/upload", tags=["Upload"])


# Get configuration from environment variables
HOST = os.getenv("BACKEND_HOST", "localhost")
PORT = int(os.getenv("BACKEND_PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )
"""
Health check endpoint for the API server.

This module provides a simple health check endpoint that can be used to:
- Monitor the API server's status
- Verify the service is running and responsive
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Basic health check endpoint.
    
    Returns:
        dict: Simple status message indicating the service is healthy
    """
    return {"status": "healthy"}
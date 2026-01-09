"""Health check router."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy"}


@router.get("/readiness")
async def readiness_check():
    """Readiness probe for Kubernetes deployments."""
    # In production, check DB connectivity, cache, etc.
    return {"status": "ready"}

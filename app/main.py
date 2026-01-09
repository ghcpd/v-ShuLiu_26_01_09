"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import todos, health

app = FastAPI(
    title="Todo API Service",
    description="A lightweight backend service for managing todo items",
    version="1.2.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(todos.router, prefix="/v1/todos", tags=["todos"])


@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Todo API Service",
        "version": "1.2.0",
        "docs": "/docs",
    }

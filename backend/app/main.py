"""
Main FastAPI application for Voryent AI Studio.
"""

from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router

app = FastAPI(
    title="Voryent AI Studio API",
    version="1.0.0",
)

app.include_router(
    api_v1_router,
    prefix="/api/v1",
)


@app.get("/health")
def health_check():
    """Basic API health check."""
    return {"status": "ok"}

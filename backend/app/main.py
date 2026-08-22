"""
Main FastAPI application for Voryent AI Studio.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import router as api_v1_router

app = FastAPI(
    title="Voryent AI Studio API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STORAGE_DIR = Path("storage/generated")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/storage/generated",
    StaticFiles(directory=str(STORAGE_DIR)),
    name="generated-images",
)

app.include_router(
    api_v1_router,
    prefix="/api/v1",
)


@app.get("/health")
def health_check():
    """Basic API health check."""
    return {"status": "ok"}
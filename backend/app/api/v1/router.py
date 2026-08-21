"""
API v1 router for Voryent AI Studio.
"""

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.generate import router as generate_router
from app.api.v1.endpoints.jobs import router as jobs_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(generate_router)
router.include_router(jobs_router)

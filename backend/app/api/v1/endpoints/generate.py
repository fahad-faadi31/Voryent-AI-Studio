"""
Image generation API endpoint.

Creates an asynchronous image generation job.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import JobService

router = APIRouter(
    prefix="/generate",
    tags=["Generation"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_generation_job(
    data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JobResponse:
    """
    Create a new image generation job.

    The authenticated user owns the created job.
    """
    job_service = JobService(db)

    job = job_service.create_job(
        user_id=current_user.id,
        prompt=data.prompt,
        aspect_ratio=data.aspect_ratio,
        seed=data.seed,
    )

    return job

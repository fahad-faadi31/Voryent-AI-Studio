"""
Job API endpoints for Voryent AI Studio.
"""

from __future__ import annotations

from math import ceil
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.job import JobListResponse, JobResponse
from app.services.job_service import JobService

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.get(
    "",
    response_model=JobListResponse,
    status_code=status.HTTP_200_OK,
)
def list_jobs(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JobListResponse:
    """
    List generation jobs belonging to the authenticated user.
    """
    job_service = JobService(db)

    jobs, total = job_service.list_jobs_for_user(
        user_id=current_user.id,
        page=page,
        limit=limit,
    )

    total_pages = ceil(total / limit) if total > 0 else 0

    return JobListResponse(
        items=jobs,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
    )


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
)
def get_job(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JobResponse:
    """
    Get a single generation job belonging to the authenticated user.
    """
    job_service = JobService(db)

    job = job_service.get_job_for_user(
        job_id=job_id,
        user_id=current_user.id,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )

    return job

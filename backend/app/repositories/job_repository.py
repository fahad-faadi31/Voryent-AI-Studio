"""
Job repository for Voryent AI Studio.

This repository encapsulates all database operations for the Job model.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.job import Job


class JobRepository:
    """Repository for Job database operations."""

    def __init__(self, db: Session):
        """Initialize with a SQLAlchemy Session."""
        self.db = db

    def create_job(
        self,
        user_id: UUID,
        prompt: str,
        aspect_ratio: str,
        seed: int | None,
    ) -> Job:
        """Create a new job in the database."""
        job = Job(
            user_id=user_id,
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            seed=seed,
            status="queued",
        )
        self.db.add(job)
        self.db.flush()
        self.db.refresh(job)
        return job

    def get_by_id(self, job_id: UUID) -> Job | None:
        """Fetch a job by its ID."""
        stmt = select(Job).where(Job.id == job_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_id_for_user(self, job_id: UUID, user_id: UUID) -> Job | None:
        """Fetch a job by ID, ensuring it belongs to the given user."""
        stmt = select(Job).where(Job.id == job_id, Job.user_id == user_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def list_by_user(
        self,
        user_id: UUID,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Job], int]:
        """List jobs for a user, paginated."""
        count_stmt = select(Job).where(Job.user_id == user_id)
        total = len(self.db.execute(count_stmt).scalars().all())

        stmt = (
            select(Job)
            .where(Job.user_id == user_id)
            .order_by(desc(Job.created_at))
            .offset((page - 1) * limit)
            .limit(limit)
        )
        jobs = self.db.execute(stmt).scalars().all()

        return list(jobs), total

    def update_status(
        self,
        job: Job,
        status: str,
        **kwargs,
    ) -> Job:
        """Update the status of a job."""
        job.status = status
        for key, value in kwargs.items():
            setattr(job, key, value)
        self.db.flush()
        self.db.refresh(job)
        return job

    def mark_processing(self, job: Job) -> Job:
        """Mark a job as processing."""
        from datetime import datetime, timezone

        job.status = "processing"
        job.started_at = datetime.now(timezone.utc)
        self.db.flush()
        self.db.refresh(job)
        return job

    def mark_completed(self, job: Job, image_url: str) -> Job:
        """Mark a job as completed with the image URL."""
        from datetime import datetime, timezone

        job.status = "completed"
        job.image_url = image_url
        job.completed_at = datetime.now(timezone.utc)
        self.db.flush()
        self.db.refresh(job)
        return job

    def mark_failed(self, job: Job, error_message: str) -> Job:
        """Mark a job as failed with an error message."""
        from datetime import datetime, timezone

        job.status = "failed"
        job.error_message = error_message
        job.completed_at = datetime.now(timezone.utc)
        self.db.flush()
        self.db.refresh(job)
        return job

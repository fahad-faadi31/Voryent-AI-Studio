"""
Job service for Voryent AI Studio.

This service coordinates the creation, retrieval, and status updates of
generation jobs. It uses JobRepository for database operations and
QueueService for enqueueing jobs.
"""

from __future__ import annotations

import random
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.job import Job
from app.repositories.job_repository import JobRepository
from app.services.queue_service import QueueService


class JobService:
    """Service for generation job business logic."""

    def __init__(self, db: Session):
        """Initialize the JobService with a database session."""
        self.db = db
        self.job_repository = JobRepository(db)
        self.queue_service = QueueService()

    def create_job(
        self,
        user_id: UUID,
        prompt: str,
        aspect_ratio: str = "1:1",
        seed: int | None = None,
    ) -> Job:
        """
        Create a new generation job and enqueue it.

        The database transaction is committed only after the job has
        successfully been added to the Redis queue.
        """
        if seed is None:
            seed = random.randint(0, 2**63 - 1)

        job = self.job_repository.create_job(
            user_id=user_id,
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            seed=seed,
        )

        enqueued = self.queue_service.enqueue_job(job.id)

        if not enqueued:
            self.db.rollback()
            raise QueueError("Failed to enqueue job. Please try again.")

        self.db.commit()

        return job

    def get_job_for_user(
        self,
        job_id: UUID,
        user_id: UUID,
    ) -> Job | None:
        """Retrieve a job belonging to the specified user."""
        return self.job_repository.get_by_id_for_user(job_id, user_id)

    def list_jobs_for_user(
        self,
        user_id: UUID,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Job], int]:
        """List jobs belonging to the specified user."""
        return self.job_repository.list_by_user(user_id, page, limit)

    def mark_processing(self, job_id: UUID) -> Job | None:
        """Mark a job as processing."""
        job = self.job_repository.get_by_id(job_id)

        if job is None:
            return None

        updated = self.job_repository.mark_processing(job)
        self.db.commit()

        return updated

    def mark_completed(
        self,
        job_id: UUID,
        image_url: str,
    ) -> Job | None:
        """Mark a job as completed."""
        job = self.job_repository.get_by_id(job_id)

        if job is None:
            return None

        updated = self.job_repository.mark_completed(
            job,
            image_url,
        )
        self.db.commit()

        return updated

    def mark_failed(
        self,
        job_id: UUID,
        error_message: str,
    ) -> Job | None:
        """Mark a job as failed."""
        job = self.job_repository.get_by_id(job_id)

        if job is None:
            return None

        updated = self.job_repository.mark_failed(
            job,
            error_message,
        )
        self.db.commit()

        return updated


class QueueError(Exception):
    """Raised when a job cannot be added to the queue."""

    def __init__(
        self,
        message: str = "Failed to enqueue job.",
    ):
        self.message = message
        super().__init__(self.message)

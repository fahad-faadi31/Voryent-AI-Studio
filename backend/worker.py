"""
Background worker for Voryent AI Studio.
"""

from __future__ import annotations

import logging
import time
from uuid import UUID

from app.db.session import SessionLocal
from app.services.job_service import JobService
from app.services.model_service import get_model_service
from app.services.queue_service import QueueService
from app.services.storage_service import StorageService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("voryent.worker")


def process_job(job_id_str: str) -> None:
    """Process one generation job."""

    job_id = UUID(job_id_str)

    logger.info("Received job: %s", job_id)

    db = SessionLocal()

    try:
        job_service = JobService(db)

        job = job_service.job_repository.get_by_id(job_id)

        if job is None:
            logger.error(
                "Job %s not found in database. Skipping.",
                job_id,
            )
            return

        job_service.mark_processing(job_id)

        logger.info(
            "Job %s marked as processing",
            job_id,
        )

        model_service = get_model_service()

        logger.info(
            "Generating image for job %s",
            job_id,
        )

        image_data = model_service.generate(
            prompt=job.prompt,
            aspect_ratio=job.aspect_ratio,
            seed=job.seed,
        )

        logger.info(
            "Image generated for job %s (%d bytes)",
            job_id,
            len(image_data),
        )

        storage_service = StorageService()

        image_path = storage_service.save_image(
            image_data=image_data,
            job_id=job_id,
            extension="png",
        )

        logger.info(
            "Image saved: %s",
            image_path,
        )

        job_service.mark_completed(
            job_id,
            image_path,
        )

        logger.info(
            "Job %s completed",
            job_id,
        )

    except Exception as exc:
        logger.error(
            "Job %s failed: %s",
            job_id,
            exc,
            exc_info=True,
        )

        try:
            job_service = JobService(db)

            job_service.mark_failed(
                job_id,
                str(exc),
            )

            logger.info(
                "Job %s marked as failed",
                job_id,
            )

        except Exception as mark_error:
            logger.error(
                "Failed to update job %s status: %s",
                job_id,
                mark_error,
            )

    finally:
        db.close()


def main() -> None:
    """Continuously process jobs from Redis."""

    logger.info("Worker started")
    logger.info("Waiting for jobs...")

    queue_service = QueueService()

    while True:
        try:
            job_id_str = queue_service.dequeue_job(
                timeout=10,
            )

            if job_id_str is None:
                continue

            process_job(job_id_str)

        except KeyboardInterrupt:
            logger.info("Worker stopped by user")
            break

        except Exception as exc:
            logger.error(
                "Unexpected worker error: %s",
                exc,
                exc_info=True,
            )

            time.sleep(1)

    logger.info("Worker shutting down")


if __name__ == "__main__":
    main()

"""
Background worker for Voryent AI Studio.
"""

from __future__ import annotations

import io
import logging
import time
from uuid import UUID

from PIL import Image, ImageDraw

from app.db.session import SessionLocal
from app.services.job_service import JobService
from app.services.queue_service import QueueService
from app.services.storage_service import StorageService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("voryent.worker")


def generate_mock_image(
    prompt: str,
    aspect_ratio: str,
    seed: int | None,
) -> bytes:
    """Generate a temporary mock PNG image."""

    dimensions = {
        "1:1": (512, 512),
        "16:9": (640, 360),
        "9:16": (360, 640),
    }

    width, height = dimensions.get(aspect_ratio, (512, 512))

    if seed is not None:
        import hashlib

        hash_value = hashlib.md5(str(seed).encode()).hexdigest()

        r = int(hash_value[0:2], 16)
        g = int(hash_value[2:4], 16)
        b = int(hash_value[4:6], 16)
    else:
        r, g, b = 100, 150, 200

    image = Image.new(
        "RGB",
        (width, height),
        color=(r, g, b),
    )

    draw = ImageDraw.Draw(image)

    border_width = 4

    draw.rectangle(
        [
            border_width,
            border_width,
            width - border_width - 1,
            height - border_width - 1,
        ],
        outline=(255, 255, 255),
        width=border_width,
    )

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="PNG",
    )

    return buffer.getvalue()


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

        logger.info(
            "Generating mock image for job %s",
            job_id,
        )

        image_data = generate_mock_image(
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

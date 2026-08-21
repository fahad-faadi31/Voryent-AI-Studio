"""
Redis queue service for Voryent AI Studio.

This service provides a clean abstraction for enqueueing and dequeuing
generation jobs. It uses Redis as the underlying message broker.
"""

from __future__ import annotations

import logging
from uuid import UUID

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)

# Queue name for generation jobs
GENERATION_QUEUE = "voryent:generation:jobs"


class QueueService:
    """Service for queueing generation jobs using Redis."""

    def __init__(self) -> None:
        """Initialize the Redis client."""
        self.redis_client = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

    def enqueue_job(self, job_id: UUID) -> bool:
        """
        Add a job ID to the generation queue.

        Args:
            job_id: UUID of the job to enqueue.

        Returns:
            True if the job was successfully queued, False otherwise.
        """
        try:
            self.redis_client.lpush(GENERATION_QUEUE, str(job_id))
            logger.info("Job %s enqueued to %s", job_id, GENERATION_QUEUE)
            return True
        except redis.RedisError as exc:
            logger.error("Failed to enqueue job %s: %s", job_id, exc)
            return False

    def dequeue_job(self, timeout: int = 0) -> str | None:
        """
        Remove and return the next job ID from the queue.

        Args:
            timeout: If > 0, block for up to this many seconds waiting for a job.
                     If 0, return immediately if queue is empty.

        Returns:
            The job ID string if available, None if queue is empty.
        """
        try:
            if timeout > 0:
                result = self.redis_client.brpop(GENERATION_QUEUE, timeout=timeout)
                if result:
                    return result[1]  # brpop returns (key, value)
                return None
            else:
                return self.redis_client.rpop(GENERATION_QUEUE)
        except redis.RedisError as exc:
            logger.error("Failed to dequeue job: %s", exc)
            return None

    def get_queue_length(self) -> int:
        """Return the current number of jobs waiting in the queue."""
        try:
            return self.redis_client.llen(GENERATION_QUEUE)
        except redis.RedisError as exc:
            logger.error("Failed to get queue length: %s", exc)
            return 0

    def ping(self) -> bool:
        """Check if Redis is reachable."""
        try:
            return self.redis_client.ping()
        except redis.RedisError:
            return False
"""
Storage service for Voryent AI Studio.

This service provides a clean abstraction for storing generated images.
The current implementation uses the local filesystem. It can be replaced
later with S3, Cloudflare R2, or other object storage without changing
the job API.
"""

from __future__ import annotations

import logging
from pathlib import Path
from uuid import UUID, uuid4

logger = logging.getLogger(__name__)

# Directory where generated images are stored
STORAGE_DIR = Path("storage/generated")


class StorageService:
    """Service for storing and retrieving generated images."""

    def __init__(self, base_dir: Path | None = None) -> None:
        """
        Initialize the storage service.

        Args:
            base_dir: Optional base directory for storage. Defaults to
                      `storage/generated` relative to the backend directory.
        """
        self.base_dir = base_dir or STORAGE_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_image(
        self,
        image_data: bytes,
        job_id: UUID,
        extension: str = "png",
    ) -> str:
        """
        Save an image and return its storage path.

        Args:
            image_data: Raw image bytes.
            job_id: UUID of the job this image belongs to.
            extension: File extension (default: png).

        Returns:
            The relative path to the saved image (e.g., "generated/abc.png").
        """
        filename = f"{uuid4()}.{extension}"
        filepath = self.base_dir / filename
        filepath.write_bytes(image_data)
        logger.info("Image saved for job %s at %s", job_id, filepath)
        return str(filepath)

    def get_image_path(self, image_path: str) -> Path | None:
        """
        Get the full path to a stored image.

        Args:
            image_path: Relative path to the image.

        Returns:
            Path object if the image exists, None otherwise.
        """
        path = Path(image_path)
        if path.exists() and path.is_file():
            return path
        return None

    def delete_image(self, image_path: str) -> bool:
        """
        Delete a stored image.

        Args:
            image_path: Relative path to the image.

        Returns:
            True if the image was deleted or did not exist, False on error.
        """
        try:
            path = Path(image_path)
            if path.exists():
                path.unlink()
                logger.info("Deleted image: %s", image_path)
            return True
        except OSError as exc:
            logger.error("Failed to delete image %s: %s", image_path, exc)
            return False
"""
Model service for Voryent AI Studio.

Provides a common interface for image generation providers.
"""

from __future__ import annotations

import hashlib
import io
import logging
from abc import ABC, abstractmethod
from typing import Any

from PIL import Image, ImageDraw

from app.core.config import settings


logger = logging.getLogger(__name__)


ASPECT_RATIOS: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "16:9": (1344, 768),
    "9:16": (768, 1344),
}


class ModelServiceError(Exception):
    """Base exception for model service errors."""


class MissingAPIKeyError(ModelServiceError):
    """Raised when the Replicate API token is missing."""


class ModelGenerationError(ModelServiceError):
    """Raised when image generation fails."""


class ModelService(ABC):
    """Common interface for all image generation providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        aspect_ratio: str,
        seed: int | None = None,
    ) -> bytes:
        """Generate an image and return PNG bytes."""
        raise NotImplementedError


class MockModelService(ModelService):
    """Local Pillow-based mock image generator."""

    def generate(
        self,
        prompt: str,
        aspect_ratio: str,
        seed: int | None = None,
    ) -> bytes:
        """Generate a simple placeholder PNG."""

        dimensions = {
            "1:1": (512, 512),
            "16:9": (640, 360),
            "9:16": (360, 640),
        }

        width, height = dimensions.get(
            aspect_ratio,
            (512, 512),
        )

        if seed is not None:
            hash_value = hashlib.md5(
                str(seed).encode()
            ).hexdigest()

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


class ReplicateModelService(ModelService):
    """Replicate-hosted image generation service."""

    def __init__(self) -> None:
        self.api_token = settings.REPLICATE_API_TOKEN
        self.model_id = settings.MODEL_ID

    def _validate_config(self) -> None:
        """Validate Replicate configuration."""

        if not self.api_token:
            raise MissingAPIKeyError(
                "REPLICATE_API_TOKEN is not configured."
            )

        if not self.model_id:
            raise ModelGenerationError(
                "MODEL_ID is not configured."
            )

    def generate(
        self,
        prompt: str,
        aspect_ratio: str,
        seed: int | None = None,
    ) -> bytes:
        """Generate an image using Replicate."""

        self._validate_config()

        if aspect_ratio not in ASPECT_RATIOS:
            raise ModelGenerationError(
                f"Unsupported aspect ratio: {aspect_ratio}"
            )

        logger.info(
            "Generating image using Replicate model %s",
            self.model_id,
        )

        model_input: dict[str, Any] = {
            "prompt": prompt,
            "resolution": "1 MP",
            "aspect_ratio": aspect_ratio,
            "output_format": "png",
            "output_quality": 90,
            "safety_tolerance": 2,
        }

        if seed is not None:
            model_input["seed"] = seed

        try:
            import replicate

            client = replicate.Client(
                api_token=self.api_token,
            )

            output = client.run(
                self.model_id,
                input=model_input,
            )

            return self._extract_output_bytes(output)

        except ModelServiceError:
            raise

        except Exception as exc:
            logger.error(
                "Replicate generation failed: %s",
                exc,
                exc_info=True,
            )

            raise ModelGenerationError(
                f"Replicate generation failed: {exc}"
            ) from exc

    @staticmethod
    def _extract_output_bytes(output: Any) -> bytes:
        """Extract image bytes from Replicate output."""

        if isinstance(output, list):
            if not output:
                raise ModelGenerationError(
                    "Replicate returned no output."
                )

            output = output[0]

        if isinstance(output, bytes):
            return output

        if hasattr(output, "read"):
            data = output.read()

            if isinstance(data, bytes):
                return data

        if isinstance(output, str):
            import httpx

            response = httpx.get(
                output,
                timeout=60.0,
                follow_redirects=True,
            )

            response.raise_for_status()

            return response.content

        if isinstance(output, dict) and "url" in output:
            import httpx

            response = httpx.get(
                output["url"],
                timeout=60.0,
                follow_redirects=True,
            )

            response.raise_for_status()

            return response.content

        raise ModelGenerationError(
            f"Unexpected Replicate output type: {type(output)}"
        )

def get_model_service() -> ModelService:
    """Return the configured model service."""

    provider = settings.MODEL_PROVIDER.lower().strip()

    if provider == "mock":
        logger.info("Using MockModelService")
        return MockModelService()

    if provider == "replicate":
        logger.info("Using ReplicateModelService")
        return ReplicateModelService()

    raise ValueError(
        f"Unknown MODEL_PROVIDER: {settings.MODEL_PROVIDER}"
    )

"""
Job schemas for Voryent AI Studio.

These schemas define the API contract for generation jobs.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    """Request schema for creating a generation job."""

    prompt: str = Field(
        min_length=1,
        max_length=500,
        description="The text prompt for image generation",
    )
    aspect_ratio: Literal["1:1", "16:9", "9:16"] = Field(
        default="1:1",
        description="Aspect ratio for the generated image",
    )
    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible generation",
    )


class JobResponse(BaseModel):
    """Response schema for a generation job."""

    id: UUID
    user_id: UUID
    prompt: str
    status: str
    aspect_ratio: str
    seed: int | None
    image_url: str | None
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class JobListResponse(BaseModel):
    """Response schema for paginated job listing."""

    items: list[JobResponse]
    total: int
    page: int
    limit: int
    total_pages: int

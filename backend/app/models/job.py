"""
Job model for Voryent AI Studio.
"""

from __future__ import annotations

import uuid

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Job(Base):
    """ORM model representing a generation job."""

    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'queued'"),
    )

    aspect_ratio: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text("'1:1'"),
    )

    seed: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    started_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="jobs",
        lazy="selectin",
    )

    __table_args__ = (
        CheckConstraint(
            "length(prompt) <= 500",
            name="ck_jobs_prompt_length",
        ),
        Index(
            "jobs_user_id_created_at_idx",
            "user_id",
            created_at.desc(),
        ),
        Index(
            "jobs_status_created_at_idx",
            "status",
            created_at.asc(),
        ),
    )

    def __repr__(self) -> str:
        return f"<Job id={self.id} status={self.status} user_id={self.user_id}>"

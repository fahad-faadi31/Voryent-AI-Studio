"""
User repository for Voryent AI Studio.

This repository encapsulates all database operations for the User model.
It uses the synchronous SQLAlchemy Session provided by app.db.session.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Repository for User database operations."""

    def __init__(self, db: Session):
        """Initialize the repository with a SQLAlchemy Session."""
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """Fetch a user by email address."""
        stmt = select(User).where(User.email == email)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_id(self, user_id: str) -> User | None:
        """Fetch a user by UUID."""
        stmt = select(User).where(User.id == user_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def create_user(self, email: str, hashed_password: str) -> User:
        """Create and persist a new user."""
        user = User(
            email=email,
            hashed_password=hashed_password,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

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
        """
        Initialize the repository with a SQLAlchemy Session.

        Args:
            db: SQLAlchemy Session for database operations.
        """
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """
        Fetch a user by their email address.

        Args:
            email: The user's email address (case-sensitive).

        Returns:
            The User object if found, otherwise None.
        """
        stmt = select(User).where(User.email == email)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_id(self, user_id: str) -> User | None:
        """
        Fetch a user by their ID.

        Args:
            user_id: The user's UUID as a string.

        Returns:
            The User object if found, otherwise None.
        """
        stmt = select(User).where(User.id == user_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def create_user(self, email: str, hashed_password: str) -> User:
        """
        Create a new user in the database.

        Args:
            email: The user's email address.
            hashed_password: The bcrypt-hashed password.

        Returns:
            The newly created User object with its database-generated ID.
        """
        user = User(
            email=email,
            hashed_password=hashed_password,
        )
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user
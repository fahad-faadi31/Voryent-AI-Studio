"""
Authentication service for Voryent AI Studio.

Handles user registration and login business logic.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class DuplicateEmailError(Exception):
    """Raised when an email is already registered."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""


class InactiveUserError(Exception):
    """Raised when an inactive user attempts to log in."""


class AuthService:
    """Business logic for authentication."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)

    async def register(self, email: str, password: str) -> User:
        """Register a new user."""

        normalized_email = email.strip().lower()

        existing_user = await self.user_repository.get_by_email(
            normalized_email
        )

        if existing_user is not None:
            raise DuplicateEmailError(
                "Email is already registered."
            )

        hashed_password = hash_password(password)

        user = await self.user_repository.create_user(
            email=normalized_email,
            hashed_password=hashed_password,
        )

        return user

    async def login(self, email: str, password: str) -> str:
        """Authenticate a user and return an access token."""

        normalized_email = email.strip().lower()

        user = await self.user_repository.get_by_email(
            normalized_email
        )

        if user is None:
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise InactiveUserError(
                "User account is inactive."
            )

        return create_access_token(str(user.id))

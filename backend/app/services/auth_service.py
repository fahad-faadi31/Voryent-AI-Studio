"""
Authentication service for Voryent AI Studio.

This service encapsulates the business logic for user registration and
login. It uses the UserRepository for database access and security
utilities for password hashing and JWT creation.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import (
    DuplicateEmailError,
    InactiveUserError,
    InvalidCredentialsError,
)
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    """Service for authentication-related business logic."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register(self, email: str, password: str) -> User:
        """Register a new user."""
        normalized_email = email.strip().lower()

        existing_user = self.user_repository.get_by_email(normalized_email)
        if existing_user is not None:
            raise DuplicateEmailError("Email is already registered.")

        hashed_password = hash_password(password)

        return self.user_repository.create_user(
            email=normalized_email,
            hashed_password=hashed_password,
        )

    def login(self, email: str, password: str) -> str:
        """Authenticate a user and return a JWT access token."""
        normalized_email = email.strip().lower()

        user = self.user_repository.get_by_email(normalized_email)
        if user is None:
            raise InvalidCredentialsError("Invalid email or password.")

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password.")

        if not user.is_active:
            raise InactiveUserError("User account is inactive.")

        return create_access_token(str(user.id))

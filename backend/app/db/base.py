"""
SQLAlchemy declarative base for Voryent AI Studio.

All ORM models must inherit from `Base`. This shared base allows Alembic
and SQLAlchemy to discover and track all tables defined in the application.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
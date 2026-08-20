"""
Database engine, session factory, and FastAPI dependency.

This module is responsible for:

- Creating the SQLAlchemy engine using DATABASE_URL from settings
- Providing a session factory for database sessions
- Providing a FastAPI dependency that yields a database session per request
"""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------
# The engine is the core SQLAlchemy object that manages connections to
# PostgreSQL. It does not connect immediately. Connections are opened lazily
# when a session first uses them.
# ---------------------------------------------------------------------------
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # Verifies connections before using them
    echo=settings.DEBUG,  # Logs SQL when debug mode is enabled
)


# ---------------------------------------------------------------------------
# Session Factory
# ---------------------------------------------------------------------------
# Sessions are the primary interface between the application and the
# database. Each request should use its own session.
# ---------------------------------------------------------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
)


# ---------------------------------------------------------------------------
# FastAPI Dependency
# ---------------------------------------------------------------------------
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    The session is created when the request starts and closed when the
    request completes, even if an error occurs.

    Yields:
        SQLAlchemy Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
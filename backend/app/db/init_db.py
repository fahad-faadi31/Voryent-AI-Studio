"""
Database initialization utilities.

Currently this provides a minimal health/connectivity check. It can be
expanded later to create initial data or perform startup maintenance.
"""

from __future__ import annotations

import logging

from sqlalchemy import text

from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Initialize the database connection and perform any required startup tasks.

    Current behaviour:
        - Verifies the database is reachable with a simple query.

    Raises:
        RuntimeError: If the database cannot be reached or queried.
    """
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Database connection verified successfully.")
    except Exception as exc:
        logger.error("Database initialization failed: %s", exc)
        raise RuntimeError("Database initialization failed") from exc
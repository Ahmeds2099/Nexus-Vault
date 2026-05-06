"""
database.py — Database engine, session management, and base model class.

Architecture note:
- Using synchronous SQLAlchemy (simpler for MVP, easier to debug)
- Session is managed per-request via FastAPI dependency injection
- Base class is imported by all models to register tables
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config import get_settings

settings = get_settings()

# ── Engine ────────────────────────────────────────────────────────────────────
# The engine is the connection pool to PostgreSQL.
# pool_pre_ping=True will automatically reconnect if the DB was restarted.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,  # Log all SQL when DEBUG=True — helpful for development
)

# ── Session Factory ───────────────────────────────────────────────────────────
# SessionLocal() creates a new database session.
# autocommit=False: we control transactions manually (commit/rollback)
# autoflush=False: we control when data is flushed to DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ── Declarative Base ──────────────────────────────────────────────────────────
# All SQLAlchemy models must inherit from this Base.
# It tracks all model classes so create_all() knows what tables to create.
Base = declarative_base()


# ── FastAPI Dependency ────────────────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session per request.
    
    Usage in routes:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    
    The 'finally' block ensures the session is ALWAYS closed,
    even if an exception is raised during the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from __future__ import annotations

from typing import Generator, Optional

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, pool_pre_ping=True) if settings.database_url else None
SessionLocal: Optional[sessionmaker] = (
    sessionmaker(bind=engine, autoflush=False, autocommit=False) if engine is not None else None
)


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise HTTPException(
            status_code=503,
            detail="Database is not configured. Set DATABASE_URL in .env.",
        )

    db = SessionLocal()
    try:
        yield db
    except OperationalError as e:
        raise HTTPException(status_code=503, detail="Database connection failure") from e
    finally:
        db.close()


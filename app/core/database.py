"""
Database configuration with async SQLAlchemy setup for PostgreSQL
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""
    pass


# Create async engine (lazy initialization)
engine = None
AsyncSessionLocal = None

def get_engine():
    """Get or create async engine"""
    global engine
    if engine is None:
        engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,  # Log SQL queries in debug mode
            future=True
        )
    return engine

def get_session_factory():
    """Get or create async session factory"""
    global AsyncSessionLocal
    if AsyncSessionLocal is None:
        AsyncSessionLocal = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False
        )
    return AsyncSessionLocal


async def get_db() -> AsyncSession:
    """
    Dependency to get database session
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """
    Initialize database tables
    """
    engine = get_engine()
    async with engine.begin() as conn:
        # Import all models to ensure they are registered
        from app.models import education
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

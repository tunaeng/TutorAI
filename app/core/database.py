from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Async engine with Supabase pooler compatibility
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    connect_args={
        "server_settings": {
            "application_name": "TutorAI Admin",
        },
        "statement_cache_size": 0,  # Disable prepared statements for Supabase pooler
    }
)

# Session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base для моделей
Base = declarative_base()

# Dependency для FastAPI
async def get_db():
    async with async_session() as session:
        yield session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings


def _ensure_asyncpg_url(url: str) -> str:
    """
    Гарантирует, что для PostgreSQL используется асинхронный драйвер asyncpg.
    Работает с форматами:
    - postgresql://...
    - postgres://...
    - postgresql+psycopg2://...
    - и уже корректным postgresql+asyncpg://...
    """
    if not url:
        raise ValueError("DATABASE_URL не установлен")

    # Уже async-драйвер
    if "+asyncpg" in url:
        return url

    # psycopg2 -> asyncpg
    if "+psycopg2" in url:
        return url.replace("+psycopg2", "+asyncpg")

    # Простые postgres/postgresql -> добавляем +asyncpg
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)

    return url


# Async engine with Supabase pooler compatibility
engine = create_async_engine(
    _ensure_asyncpg_url(settings.DATABASE_URL),
    echo=settings.DEBUG,
    future=True,
    connect_args={
        "server_settings": {
            "application_name": "TutorAI Admin",
        },
        "statement_cache_size": 0,  # Disable prepared statements for Supabase pooler
    },
)

# Session factory для async
async_session = async_sessionmaker(
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
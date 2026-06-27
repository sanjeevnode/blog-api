from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.logger import escape_log_braces, get_logger

logger = get_logger()


# Create the asynchronous engine
engine = create_async_engine(
    settings.get_database_url,
    echo=False,             # Set to True if you want to print all SQL statements to logs
    future=True,
    pool_pre_ping=True,     # Liveness probe to check connections before using them
    pool_size=5,            # Number of persistent connections
    max_overflow=10,        # Temporary connections in spikes
    pool_recycle=1800,      # Recycle connections after 30 minutes
)

# Setup async session factory
async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection helper to yield DB sessions.
    Automatically handles transaction commit on success, rollback on failure,
    and session closure.
    """
    session = async_session_factory()
    try:
        yield session
        await session.commit()
    except Exception as exc:
        await session.rollback()
        logger.error(f"db session error: {escape_log_braces(exc)}")
        raise
    finally:
        await session.close()
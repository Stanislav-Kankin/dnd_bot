from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from config import settings

# Асинхронный движок для SQLite
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Асинхронная сессия
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Генератор асинхронных сессий."""
    async with AsyncSessionLocal() as session:
        yield session

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from database.models import Base


async def create_database():
    engine = create_async_engine("sqlite+aiosqlite:///dnd_bot.db", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_database())

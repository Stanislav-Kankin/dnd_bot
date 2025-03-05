from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User


class CharacterManager:
    @staticmethod
    async def create_user(session: AsyncSession, telegram_id: int, username: str) -> User:
        """Создание нового пользователя."""
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get_user(session: AsyncSession, telegram_id: int) -> User:
        """Получение пользователя по telegram_id."""
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalars().first()

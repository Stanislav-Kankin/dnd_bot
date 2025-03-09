from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Character
from database.models import User


class CharacterManager:
    @staticmethod
    async def create_character(session: AsyncSession, user_id: int, character_data: dict) -> Character:
        """Создание нового персонажа."""
        character = Character(user_id=user_id, **character_data)
        session.add(character)
        await session.commit()
        await session.refresh(character)
        return character

    @staticmethod
    async def update_character(session: AsyncSession, character_id: int, character_data: dict) -> Character:
        """Обновление персонажа."""
        character = await session.get(Character, character_id)
        if character:
            for key, value in character_data.items():
                setattr(character, key, value)
            await session.commit()
            await session.refresh(character)
        return character

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

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User


class CharacterManager:
    @staticmethod
    async def create_character(session: AsyncSession, user_id: int, character_data: dict) -> dict:
        """Создание нового персонажа."""
        user = await CharacterManager.get_user(session, user_id)
        if not user:
            return None

        if not user.characters:
            user.characters = []

        user.characters.append(character_data)
        await session.commit()
        await session.refresh(user)
        return character_data

    @staticmethod
    async def update_character(session: AsyncSession, user_id: int, character_id: int, character_data: dict) -> dict:
        """Обновление персонажа."""
        user = await CharacterManager.get_user(session, user_id)
        if not user or not user.characters or character_id >= len(user.characters):
            return None

        user.characters[character_id] = character_data
        await session.commit()
        await session.refresh(user)
        return character_data

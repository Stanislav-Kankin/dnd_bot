from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import GameSession


class SessionManager:
    @staticmethod
    async def create_session(session: AsyncSession, dm_id: int, name: str) -> GameSession:
        """Создание новой игровой сессии."""
        game_session = GameSession(dm_id=dm_id, name=name)
        session.add(game_session)
        await session.commit()
        await session.refresh(game_session)
        return game_session

    @staticmethod
    async def get_session(session: AsyncSession, session_id: int) -> GameSession:
        """Получение игровой сессии по ID."""
        result = await session.execute(select(GameSession).where(GameSession.id == session_id))
        return result.scalars().first()

    @staticmethod
    async def add_player(session: AsyncSession, game_session: GameSession, player_id: int) -> None:
        """Добавление игрока в сессию."""
        if player_id not in game_session.players:
            game_session.players.append(player_id)
            await session.commit()
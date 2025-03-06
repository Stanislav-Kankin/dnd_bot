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

    @staticmethod
    async def add_monster(session: AsyncSession, session_id: int, monster_data: dict) -> None:
        """Добавление монстра в сессию."""
        game_session = await SessionManager.get_session(session, session_id)
        if game_session:
            if "monsters" not in game_session.current_initiative:
                game_session.current_initiative["monsters"] = []
            game_session.current_initiative["monsters"].append(monster_data)
            await session.commit()

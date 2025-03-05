from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.session_manager import SessionManager
from database import get_db

router = Router()


@router.message(Command("dm"))
async def dm_command(message: Message):
    """Обработчик команды /dm."""
    await message.answer(
        "Режим Dungeon Master:\n"
        "/create_session <название> - Создать сессию\n"
        "/add_player <id_сессии> <id_игрока> - Добавить игрока\n"
        "/start_session <id_сессии> - Начать сессию"
    )


@router.message(Command("create_session"))
async def create_session(message: Message):
    """Создание новой игровой сессии."""
    session_name = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else "Новая сессия"
    async for db_session in get_db():
        game_session = await SessionManager.create_session(db_session, message.from_user.id, session_name)
        await message.answer(f"Сессия '{game_session.name}' создана! ID: {game_session.id}")


@router.message(Command("add_player"))
async def add_player(message: Message):
    """Добавление игрока в сессию."""
    try:
        _, session_id, player_id = message.text.split()
        async for db_session in get_db():
            game_session = await SessionManager.get_session(db_session, int(session_id))
            if game_session:
                await SessionManager.add_player(db_session, game_session, int(player_id))
                await message.answer(f"Игрок {player_id} добавлен в сессию '{game_session.name}'!")
            else:
                await message.answer("Сессия не найдена.")
    except ValueError:
        await message.answer("Используйте: /add_player <id_сессии> <id_игрока>")
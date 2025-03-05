from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from services.session_manager import SessionManager
from database import get_db

router = Router()


@router.message(Command("dm"))
async def dm_command(message: Message):
    """Обработчик команды /dm."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать сессию 🖋️", callback_data="create_session")],
        [InlineKeyboardButton(text="Добавить игрока 🙋‍♂️", callback_data="add_player")],
        [InlineKeyboardButton(text="Управление инициативой ⚔️", callback_data="manage_initiative")]
    ])
    await message.answer(
        "Режим Dungeon Master:\n"
        "Выберите действие:",
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data == "create_session")
async def create_session(callback_query: CallbackQuery):
    """Создание новой игровой сессии."""
    async for session in get_db():
        game_session = await SessionManager.create_session(session, callback_query.from_user.id, "Новая сессия")
        await callback_query.message.answer(f"Сессия '{game_session.name}' создана! ID: {game_session.id}")


@router.callback_query(lambda c: c.data == "add_player")
async def add_player(callback_query: CallbackQuery):
    """Добавление игрока в сессию."""
    await callback_query.message.answer("Введите ID игрока:")
    # Здесь можно добавить логику для ожидания ввода ID игрока


@router.callback_query(lambda c: c.data == "manage_initiative")
async def manage_initiative(callback_query: CallbackQuery):
    """Управление инициативой."""
    async for session in get_db():
        game_session = await SessionManager.get_session(session, callback_query.from_user.id)
        if game_session:
            initiative_order = "\n".join([f"{i + 1}. {player}" for i, player in enumerate(game_session.current_initiative)])
            await callback_query.message.answer(f"Текущая инициатива:\n{initiative_order}")
        else:
            await callback_query.message.answer("Сессия не найдена.")

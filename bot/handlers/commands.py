from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from services.character_manager import CharacterManager
from database import get_db

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    """Обработчик команды /start."""
    async for session in get_db():
        user = await CharacterManager.get_user(session, message.from_user.id)
        if not user:
            user = await CharacterManager.create_user(
                session,
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
            await message.answer(f"Добро пожаловать, {user.username}! Вы успешно зарегистрированы.")
        else:
            await message.answer(f"С возвращением, {user.username}!")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мой персонаж 🧙‍♂️", callback_data="my_character")],
        [InlineKeyboardButton(text="Бросить кубик 🎲", callback_data="roll_dice")],
        [InlineKeyboardButton(text="Режим ДМа 🐉", callback_data="dm_mode")]
    ])
    await message.answer(
        "Выберите действие:",
        reply_markup=keyboard
    )



@router.callback_query(lambda c: c.data == "register")
async def register_user(callback_query: CallbackQuery):
    """Обработчик регистрации."""
    async for session in get_db():
        user = await CharacterManager.get_user(session, callback_query.from_user.id)
        if not user:
            user = await CharacterManager.create_user(
                session,
                telegram_id=callback_query.from_user.id,
                username=callback_query.from_user.username
            )
            await callback_query.message.answer(f"Пользователь {user.username} успешно зарегистрирован!")
        else:
            await callback_query.message.answer(f"Вы уже зарегистрированы как {user.username}!")


@router.callback_query(lambda c: c.data == "my_character")
async def my_character(callback_query: CallbackQuery):
    """Меню управления персонажем."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Просмотр характеристик 📊", callback_data="view_stats")],
        [InlineKeyboardButton(text="Редактировать характеристики ✏️", callback_data="edit_stats")],
        [InlineKeyboardButton(text="Инвентарь 🎒", callback_data="inventory")],
        [InlineKeyboardButton(text="Заметки 📝", callback_data="notes")],
        [InlineKeyboardButton(text="Удалить персонажа ❌", callback_data="delete_character")]
    ])
    await callback_query.message.answer(
        "Управление персонажем:",
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data == "dm_mode")
async def dm_mode(callback_query: CallbackQuery):
    """Меню ДМа."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать сессию 🖋️", callback_data="create_session")],
        [InlineKeyboardButton(text="Добавить игрока 🙋‍♂️", callback_data="add_player")],
        [InlineKeyboardButton(text="Добавить монстра 🐉", callback_data="add_monster")],
        [InlineKeyboardButton(text="Управление инициативой ⚔️", callback_data="manage_initiative")],
        [InlineKeyboardButton(text="Управление боем 🛡️", callback_data="manage_combat")]
    ])
    await callback_query.message.answer(
        "Режим ДМа:",
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data == "manage_combat")
async def manage_combat(callback_query: CallbackQuery):
    """Управление боем."""
    async for session in get_db():
        game_session = await SessionManager.get_session(session, callback_query.from_user.id)
        if game_session:
            initiative_order = "\n".join([f"{i + 1}. {player}" for i, player in enumerate(game_session.current_initiative)])
            await callback_query.message.answer(
                f"Текущая инициатива:\n{initiative_order}\n\n"
                "Выберите действие:",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Завершить ход ✅", callback_data="end_turn")],
                    [InlineKeyboardButton(text="Атаковать ⚔️", callback_data="attack")],
                    [InlineKeyboardButton(text="Использовать заклинание 🔮", callback_data="cast_spell")]
                ])
            )
        else:
            await callback_query.message.answer("Сессия не найдена.")


@router.callback_query(lambda c: c.data == "roll_dice")
async def roll_dice(callback_query: CallbackQuery):
    """Бросок кубика."""
    import random
    result = random.randint(1, 20)
    await callback_query.message.answer(f"🎲 Вы бросили кубик: {result}")
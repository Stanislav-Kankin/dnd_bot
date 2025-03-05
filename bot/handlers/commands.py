from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from services.character_manager import CharacterManager
from database import get_db

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    """Обработчик команды /start."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Регистрация 🖋️", callback_data="register")],
        [InlineKeyboardButton(text="Мой персонаж 🧙‍♂️", callback_data="my_character")],
        [InlineKeyboardButton(text="Бросить кубик 🎲", callback_data="roll_dice")]
    ])
    await message.answer(
        "Добро пожаловать в D&D бота!\n\n"
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
    """Просмотр персонажа."""
    async for session in get_db():
        user = await CharacterManager.get_user(session, callback_query.from_user.id)
        if user and user.characters:
            character = user.characters[user.current_character] if user.current_character else user.characters[0]
            await callback_query.message.answer(
                f"Персонаж: {character['name']}\n"
                f"Класс: {character['class']}\n"
                f"Уровень: {character['level']}\n"
                f"Инвентарь: {', '.join(character['inventory'])}"
            )
        else:
            await callback_query.message.answer("У вас пока нет персонажей.")


@router.callback_query(lambda c: c.data == "roll_dice")
async def roll_dice(callback_query: CallbackQuery):
    """Бросок кубика."""
    import random
    result = random.randint(1, 20)
    await callback_query.message.answer(f"🎲 Вы бросили кубик: {result}")

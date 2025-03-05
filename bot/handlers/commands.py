from aiogram import Router
from aiogram.types import (
    Message, InlineKeyboardMarkup,
    InlineKeyboardButton, CallbackQuery
    )
from aiogram.filters import Command
from services.character_manager import CharacterManager
from database import get_db

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    """Обработчик команды /start."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Регистрация 🖋️", callback_data="register")],
        [InlineKeyboardButton(text="Режим ДМа 🌍", callback_data="dm_mode")]
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
            await callback_query.message.answer(
                f"Пользователь {user.username} успешно зарегистрирован!"
                )
        else:
            await callback_query.message.answer(
                f"Вы уже зарегистрированы как {user.username}!"
                )

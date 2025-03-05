from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.character_manager import CharacterManager
from database import get_db

router = Router()


@router.message(Command("register"))
async def register_user(message: Message):
    async with get_db() as session:
        user = await CharacterManager.get_user(session, message.from_user.id)
        if not user:
            user = await CharacterManager.create_user(
                session,
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
            await message.answer(
                f"Пользователь {user.username} успешно зарегистрирован!"
                )
        else:
            await message.answer(
                f"Вы уже зарегистрированы как {user.username}!"
                )

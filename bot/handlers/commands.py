from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from services.character_manager import CharacterManager
from aiogram.types import WebAppInfo

from services.parser import DnDParser
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


@router.message(Command("spell"))
async def search_spell(message: Message):
    """Поиск заклинания."""
    spell_name = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not spell_name:
        await message.answer("Введите название заклинания.")
        return

    spell = await DnDParser.get_spell(spell_name)
    if spell:
        await message.answer(
            f"Заклинание: {spell['name']}\n"
            f"Описание: {spell['description']}"
        )
    else:
        await message.answer("Заклинание не найдено.")


@router.message(Command("class"))
async def search_class(message: Message):
    """Поиск класса."""
    class_name = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not class_name:
        await message.answer("Введите название класса.")
        return

    class_info = await DnDParser.get_class(class_name)
    if class_info:
        await message.answer(
            f"Класс: {class_info['name']}\n"
            f"Описание: {class_info['description']}"
        )
    else:
        await message.answer("Класс не найден.")


@router.callback_query(lambda c: c.data == "create_character")
async def create_character(callback_query: CallbackQuery):
    """Создание персонажа."""
    character_data = {
        "name": "Новый персонаж",
        "class": "Воин",
        "level": 1,
        "inventory": []
    }
    async for session in get_db():
        character = await CharacterManager.create_character(session, callback_query.from_user.id, character_data)
        if character:
            await callback_query.message.answer(f"Персонаж {character['name']} создан!")
        else:
            await callback_query.message.answer("Ошибка при создании персонажа.")


@router.message(Command("wiki"))
async def wiki_command(message: Message):
    """Обработчик команды /wiki."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Заклинания",
            web_app=WebAppInfo(url="https://dnd.su/spells/")
        )],
        [InlineKeyboardButton(
            text="Магические предметы",
            web_app=WebAppInfo(url="https://dnd.su/items/")
        )],
        [InlineKeyboardButton(
            text="Бестиарий",
            web_app=WebAppInfo(url="https://dnd.su/bestiary/")
        )],
        [InlineKeyboardButton(
            text="Расы",
            web_app=WebAppInfo(url="https://dnd.su/race/")
        )],
        [InlineKeyboardButton(
            text="Классы",
            web_app=WebAppInfo(url="https://dnd.su/class/")
        )],
        [InlineKeyboardButton(
            text="Главная ДнД Вики",
            web_app=WebAppInfo(url="https://dnd.su/")
        )]
    ])
    await message.answer(
        "Выберите меню:",
        reply_markup=keyboard
    )

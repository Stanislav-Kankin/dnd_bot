from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

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


@router.callback_query(lambda c: c.data == "add_monster")
async def add_monster(callback_query: CallbackQuery):
    """Добавление монстра."""
    monster_data = {
        "name": "Гоблин",
        "hp": 10,
        "ac": 15
    }
    async for session in get_db():
        await SessionManager.add_monster(session, callback_query.from_user.id, monster_data)
        await callback_query.message.answer(f"Монстр {monster_data['name']} добавлен!")


class MonsterCreation(StatesGroup):
    name = State()
    hp = State()
    ac = State()
    attack_dice = State()


@router.callback_query(lambda c: c.data == "add_monster")
async def start_monster_creation(callback_query: CallbackQuery, state: FSMContext):
    """Начало создания монстра."""
    await callback_query.message.answer("Введите название монстра:")
    await state.set_state(MonsterCreation.name)


@router.message(MonsterCreation.name)
async def process_name(message: Message, state: FSMContext):
    """Обработка названия монстра."""
    await state.update_data(name=message.text)
    await message.answer("Введите количество очков здоровья (HP):")
    await state.set_state(MonsterCreation.hp)


@router.message(MonsterCreation.hp)
async def process_hp(message: Message, state: FSMContext):
    """Обработка HP монстра."""
    await state.update_data(hp=int(message.text))
    await message.answer("Введите класс защиты (AC):")
    await state.set_state(MonsterCreation.ac)


@router.message(MonsterCreation.ac)
async def process_ac(message: Message, state: FSMContext):
    """Обработка AC монстра."""
    await state.update_data(ac=int(message.text))
    await message.answer("Введите атаку (грани кубика и количество, например, '20 1'):")
    await state.set_state(MonsterCreation.attack_dice)


@router.message(MonsterCreation.attack_dice)
async def process_attack_dice(message: Message, state: FSMContext):
    """Обработка атаки монстра."""
    dice, count = map(int, message.text.split())
    data = await state.get_data()
    monster_data = {
        "name": data["name"],
        "hp": data["hp"],
        "ac": data["ac"],
        "attack_dice": {"dice": dice, "count": count}
    }
    async for session in get_db():
        await SessionManager.add_monster(session, message.from_user.id, monster_data)
        await message.answer(f"Монстр {monster_data['name']} создан!")
    await state.clear()

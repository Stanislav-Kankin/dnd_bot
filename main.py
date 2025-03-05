import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import settings
from database import get_db

# Инициализация бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Добро пожаловать в D&D бота! Используйте /help для списка команд.")


# Команда /help
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Список команд:\n/start - Начать\n/help - Помощь")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from aiogram import Bot, Dispatcher
from config import settings
from bot.handlers import commands, dm

# Инициализация бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

dp.include_router(commands.router)
dp.include_router(dm.router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

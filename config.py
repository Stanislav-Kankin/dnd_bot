from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str = "sqlite+aiosqlite:///dnd_bot.db"

    class Config:
        env_file = ".env"


settings = Settings()

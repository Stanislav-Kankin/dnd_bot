from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(50), nullable=True)
    characters = Column(JSON, default=[])
    current_character = Column(Integer, nullable=True)


class GameSession(Base):
    __tablename__ = 'game_sessions'
    id = Column(Integer, primary_key=True)
    dm_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ID ДМа
    name = Column(String(100), nullable=False)  # Название сессии
    players = Column(JSON, default=[])  # Список игроков (их telegram_id)
    current_initiative = Column(JSON, default=[])  # Текущая инициатива
"""
Модуль настройки SQLAlchemy.

Описывает БД и определяет асинхронную сессию для
подсоединения к ней.
"""
import os

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.ext.declarative import declarative_base

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
db_file = os.path.join(parent_dir, 'app.db')

DATABASE_URL = f"sqlite+aiosqlite:///{db_file}"

engine = create_async_engine(DATABASE_URL, echo=True)
# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


session = async_session()
Base = declarative_base()

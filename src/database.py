# src/database.py

import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings as global_settings

# Настроить логгер SQLAlchemy
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

engine = create_async_engine(
    global_settings.asyncpg_url,
    future=True,
    echo=False,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionFactory() as session:
        yield session

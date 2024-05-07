from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings as global_settings

engine = create_async_engine(
    global_settings.asyncpg_url,
    future=True,
    echo=True,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionFactory() as session:
        yield session

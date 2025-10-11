from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL, query_cache_size=3600,  pool_size=100, max_overflow=10)
session_local = sessionmaker(bind=engine)


@contextmanager
def session_manager():
    with session_local() as session:
        with session.begin():
            yield session


from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager


async_engine = create_async_engine(
    (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    ),
    pool_size=100,
    max_overflow=10,
    query_cache_size=3600
)

async_session_local = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def async_session_manager() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_local() as async_session:
        async with async_session.begin():
            yield async_session

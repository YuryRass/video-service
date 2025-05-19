import asyncio

import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.database.database import Base

TEST_DB_URL = "sqlite+aiosqlite:///tests/test_db.sqlite"

test_async_engine = create_async_engine(TEST_DB_URL)
test_async_session = async_sessionmaker(test_async_engine)
test_scoped_session = async_scoped_session(
    test_async_session,
    scopefunc=asyncio.current_task,
)


@pytest_asyncio.fixture(autouse=True, scope="function")
async def init_models(event_loop):
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

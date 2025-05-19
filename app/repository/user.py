from dataclasses import dataclass
from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def create_user(self, **data: Any) -> None:
        query = insert(User).values(**data)
        session: AsyncSession
        async with self.db_session() as session:
            await session.execute(query)
            await session.commit()

    async def get_user(self, **kwargs: Any) -> User | None:
        query = select(User).filter_by(**kwargs)
        session: AsyncSession
        async with self.db_session() as session:
            user = await session.execute(query)
            return user.scalar_one_or_none()

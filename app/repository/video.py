from dataclasses import dataclass
from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Video


@dataclass
class VideoRepository:
    db_session: AsyncSession

    async def create_video(self, **data: Any) -> Video:
        query = insert(Video).values(**data).returning(Video)
        session: AsyncSession
        async with self.db_session() as session:
            res = await session.execute(query)
            await session.commit()
            return res.scalar_one()

    async def get_video(self, **kwargs: Any) -> Video | None:
        query = select(Video).filter_by(**kwargs)
        session: AsyncSession
        async with self.db_session() as session:
            user = await session.execute(query)
            return user.scalar_one_or_none()

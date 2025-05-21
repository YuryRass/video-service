from dataclasses import dataclass
from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.database import test_scoped_session
from tests.fixtures.video.video_model import VideoFactory


@dataclass
class FakeVideoRepository:
    db_session: AsyncSession
    video_obj = None

    async def get_video(self, **kwargs: Any) -> Any | None:
        return self.video_obj

    async def create_video(self, **video_data: Any) -> VideoFactory:
        self.video_obj = VideoFactory.create(**video_data)
        return self.video_obj


@pytest.fixture
def fake_video_repository() -> FakeVideoRepository:
    return FakeVideoRepository(test_scoped_session)

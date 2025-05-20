import pytest_asyncio

from app.service.video import VideoService
from app.settings import Settings
from tests.fixtures.video.video_cache_repository import FakeVideoCache
from tests.fixtures.video.video_repository import FakeVideoRepository


@pytest_asyncio.fixture
async def mock_video_service(
    fake_video_repository: FakeVideoRepository,
    fake_video_cache_repository: FakeVideoCache,
) -> VideoService:
    return VideoService(
        video_repository=fake_video_repository,
        video_cache_repository=fake_video_cache_repository,
        settings=Settings(),
    )

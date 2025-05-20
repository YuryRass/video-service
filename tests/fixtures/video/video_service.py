import pytest_asyncio

from app.repository.cache_video import VideoCache
from app.repository.video import VideoRepository
from app.service.video import VideoService
from app.settings import Settings


@pytest_asyncio.fixture
async def mock_video_service(
    fake_video_repository: VideoRepository,
    fake_video_cache_repository: VideoCache,
) -> VideoService:
    return VideoService(
        video_repository=fake_video_repository,
        video_cache_repository=fake_video_cache_repository,
        settings=Settings(),
    )

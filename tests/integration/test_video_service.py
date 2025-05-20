from unittest.mock import MagicMock

import pytest

from app.repository.user import UserRepository
from app.repository.video import VideoRepository
from app.schema.video import VideoCreateSchema, VideoResponseSchema
from app.service.video import VideoService

pytestmark = pytest.mark.asyncio

TEST_VIDEO_TITLE = "test_title"
TEST_TEMPLATE_URL = "http://example.com"


async def test_video_service(
    mock_video_service: VideoService,
    fake_user_repository: UserRepository,
    fake_video_repository: VideoRepository,
):
    await fake_user_repository.create_user()
    created_user = await fake_user_repository.get_user()
    mock_background_tasks = MagicMock()
    created_video = await mock_video_service.create_video(
        video_data=VideoCreateSchema(
            user_id=created_user.id,
            title=TEST_VIDEO_TITLE,
            url=f"{TEST_TEMPLATE_URL}/video.mp4",
        ),
        background_tasks=mock_background_tasks,
    )

    assert created_video.title == TEST_VIDEO_TITLE
    assert (
        created_video.playlist_url
        == f"{TEST_TEMPLATE_URL}/hls/{created_video.id}.m3u8"
    )

    finded_video = await mock_video_service.get_video(
        video_id=created_video.id,
        user_id=created_user.id,
    )
    assert VideoResponseSchema.model_validate(created_video) == finded_video

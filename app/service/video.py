from dataclasses import dataclass

from fastapi import BackgroundTasks

from app.repository.cache_video import VideoCache
from app.repository.video import VideoRepository
from app.schema.video import VideoCreateSchema, VideoResponseSchema
from app.settings import Settings
from app.tasks.generate_hls import generate_hls


@dataclass
class VideoService:
    video_repository: VideoRepository
    video_cache_repository: VideoCache
    settings: Settings

    async def create_video(
        self,
        video_data: VideoCreateSchema,
        background_tasks: BackgroundTasks,
    ) -> VideoResponseSchema:
        video = await self.video_repository.create_video(
            **video_data.model_dump(),
        )
        await self.video_cache_repository.set_video_for_user(video)
        background_tasks.add_task(generate_hls, video.id)
        return VideoResponseSchema.model_validate(video)

    async def get_video(
        self, video_id: int, user_id: int
    ) -> VideoResponseSchema | None:
        video = await self.video_cache_repository.get_video_by_user(
            video_id,
            user_id,
        )
        if not video:
            if video := await self.video_repository.get_video(
                id=video_id,
                user_id=user_id,
            ):
                await self.video_cache_repository.set_video_for_user(video)
        return video

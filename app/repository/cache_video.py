import json

from redis.asyncio import Redis

from app.models.video import Video
from app.schema.video import VideoResponseSchema


class VideoCache:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.redis_key_template = "{video_id}_{user_id}"

    async def get_video_by_user(
        self,
        video_id: int,
        user_id: int,
    ) -> VideoResponseSchema | None:
        if video_result := await self.redis.get(
            self._get_key(
                video_id,
                user_id,
            )
        ):
            return VideoResponseSchema.model_validate(json.loads(video_result))

    async def set_video_for_user(self, video: Video) -> None:
        video_schema = VideoResponseSchema.model_validate(video)
        await self.redis.set(
            self._get_key(video.id, video.user_id),
            video_schema.model_dump_json(),
        )

    def _get_key(self, video_id: int, user_id: int) -> str:
        return self.redis_key_template.format(
            video_id=video_id,
            user_id=user_id,
        )

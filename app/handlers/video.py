from fastapi import APIRouter, BackgroundTasks, Depends

from app.dependencies import get_current_user, get_video_service
from app.models.user import User
from app.schema.video import (CacheVideoResponseSchema, HttpPostVideoSchema,
                              VideoCreateSchema, VideoResponseSchema)
from app.service.video import VideoService

router: APIRouter = APIRouter(tags=["Video"])


@router.post(
    "/videos",
    summary="Добавление нового видео",
    response_model=VideoResponseSchema,
)
async def create_video(
    video_data: HttpPostVideoSchema,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> VideoResponseSchema:
    """Создание видео."""
    new_video = VideoCreateSchema(
        **video_data.model_dump(),
        user_id=current_user.id,
    )
    return await video_service.create_video(new_video, background_tasks)


@router.get(
    "/videos/{video_id}",
    summary="Получение видео по ID",
)
async def get_video(
    video_id: int,
    current_user: User = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> VideoResponseSchema | CacheVideoResponseSchema | None:
    """Получение видео."""
    return await video_service.get_video(video_id, current_user.id)

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.cache.accessor import get_cache
from app.infrastructure.database.accessor import get_db_session
from app.models.user import User
from app.repository.cache_video import VideoCache
from app.repository.user import UserRepository
from app.repository.video import VideoRepository
from app.service.auth import AuthService
from app.service.user import UserService
from app.service.video import VideoService
from app.settings import Settings, get_settings


async def get_user_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    return AuthService(user_repo, settings)


async def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
    settings: Settings = Depends(get_settings),
) -> UserService:
    return UserService(user_repo, settings)


async def get_current_user(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    return await auth_service.get_user_from_access_token(request)


async def get_video_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> VideoRepository:
    return VideoRepository(db_session)


async def get_video_cache_repository(
    redis_cache=Depends(get_cache),
) -> VideoCache:
    return VideoCache(redis_cache)


async def get_video_service(
    settings: Settings = Depends(get_settings),
    video_repo: VideoRepository = Depends(get_video_repository),
    video_cache_repo: VideoCache = Depends(get_video_cache_repository),
) -> VideoService:
    return VideoService(video_repo, video_cache_repo, settings)

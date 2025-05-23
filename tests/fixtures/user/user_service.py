import pytest_asyncio

from app.repository.user import UserRepository
from app.service.user import UserService
from app.settings import Settings


@pytest_asyncio.fixture
async def mock_user_service(
    fake_user_repository: UserRepository,
) -> UserService:
    return UserService(
        user_repository=fake_user_repository,
        settings=Settings(),
    )

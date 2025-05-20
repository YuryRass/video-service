import pytest_asyncio

from app.service.user import UserService
from app.settings import Settings
from tests.fixtures.user.user_repository import FakeUserRepository


@pytest_asyncio.fixture
async def mock_user_service(
    fake_user_repository: FakeUserRepository,
) -> UserService:
    return UserService(
        user_repository=fake_user_repository,
        settings=Settings(),
    )

import pytest

from app.repository.user import UserRepository
from app.schema.user import UserCreateSchema
from app.service.user import UserService

pytestmark = pytest.mark.asyncio

TEST_EMAIL = "test@mail.ru"
TEST_PASSWORD = "blabla"


async def test_user_service(
    mock_user_service: UserService,
    fake_user_repository: UserRepository,
):
    await mock_user_service.register(
        user_data=UserCreateSchema(
            email=TEST_EMAIL,
            password=TEST_PASSWORD,
        )
    )
    user = await fake_user_repository.get_user()
    assert user.email == TEST_EMAIL
    assert user.password == TEST_PASSWORD

    current_user = await mock_user_service.read_users_me(user)
    assert current_user.email == TEST_EMAIL
    assert current_user.id == user.id

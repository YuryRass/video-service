from dataclasses import dataclass
from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.database import test_scoped_session
from tests.fixtures.user.user_model import UserFactory


@dataclass
class FakeUserRepository:
    db_session: AsyncSession
    user_obj = None

    async def get_user(self, **kwargs: Any) -> Any | None:
        return self.user_obj

    async def create_user(self, **user_data: Any) -> None:
        self.user_obj = UserFactory.create(**user_data)


@pytest.fixture
def fake_user_repository() -> FakeUserRepository:
    return FakeUserRepository(test_scoped_session)

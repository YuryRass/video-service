import asyncio

import pytest

pytest_plugins = [
    "tests.fixtures.user.user_repository",
    "tests.fixtures.user.user_model",
    "tests.fixtures.user.user_service",
    "tests.database",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

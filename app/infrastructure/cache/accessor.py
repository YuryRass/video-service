from typing import AsyncGenerator

from redis.asyncio import ConnectionPool, Redis

from app.settings import get_settings


class RedisCache:
    def __init__(self):
        pool = ConnectionPool.from_url(get_settings().redis_url)
        self.redis = Redis(connection_pool=pool)


redis_cache = RedisCache()


async def get_cache() -> AsyncGenerator[Redis, None]:
    async with redis_cache.redis as redis:
        yield redis

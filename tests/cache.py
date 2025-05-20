class FakeRedis:
    def __init__(self):
        self.storage = {}

    async def get(self, key: str) -> str | None:
        return self.storage.get(key)

    async def set(self, key: str, value: str) -> None:
        self.storage[key] = value

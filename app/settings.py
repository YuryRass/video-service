from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_DRIVER: str
    DB_NAME: str

    CACHE_HOST: str
    CACHE_PORT: int
    CACHE_DB: int
    JWT_SECRET_KEY: str
    JWT_ENCODE_ALGORITHM: str
    JWT_COOKIE_KEY: str

    HLS_URL_TEMPLATE: str
    LOCAL_PATH_TO_HLS: str

    @property
    def db_url(self) -> str:
        return (
            f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def redis_url(self) -> str:
        """URL адрес Redis."""
        return f"redis://{self.CACHE_HOST}:{self.CACHE_PORT}/{self.CACHE_DB}"

    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> Settings:
    return Settings()

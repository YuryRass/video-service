from urllib.parse import urljoin

from pydantic import BaseModel, HttpUrl, computed_field, field_validator

from app.settings import get_settings


class HttpPostVideoSchema(BaseModel):
    title: str
    url: HttpUrl


class VideoCreateSchema(BaseModel):
    user_id: int
    title: str
    url: HttpUrl

    @field_validator("url", mode="after")
    @classmethod
    def validate_url(cls, val: HttpUrl) -> str:
        return str(val)


class VideoResponseSchema(BaseModel):
    id: int
    title: str

    @computed_field
    def playlist_url(self) -> str:
        return urljoin(get_settings().HLS_URL_TEMPLATE, f"{self.id}.m3u8")

    class Config:
        from_attributes = True
        extra = "ignore"

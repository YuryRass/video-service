import urllib.parse

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    computed_field,
    field_validator,
)


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
    url: HttpUrl | None = Field(None, exclude=True)

    @computed_field
    def playlist_url(self) -> str:
        parsed_url = urllib.parse.urlparse(str(self.url))

        new_path = f"/hls/{self.id}.m3u8"

        new_url = urllib.parse.urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                new_path,
                parsed_url.params,
                parsed_url.query,
                parsed_url.fragment,
            )
        )

        return new_url

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str

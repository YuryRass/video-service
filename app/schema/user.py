from pydantic import BaseModel, EmailStr


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
        extra = "ignore"


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str

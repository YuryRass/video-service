from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from app.exceptions import EmailIsAllredyExist
from app.models.user import User
from app.repository.user import UserRepository
from app.schema.user import UserCreateSchema, UserResponseSchema
from app.settings import Settings


@dataclass
class UserService:
    user_repository: UserRepository
    settings: Settings

    async def register(self, user_data: UserCreateSchema) -> None:
        try:
            await self.user_repository.create_user(**user_data.model_dump())
        except IntegrityError:
            raise EmailIsAllredyExist

    async def read_users_me(
        self,
        current_user: User,
    ) -> UserResponseSchema:
        return UserResponseSchema.model_validate(current_user)

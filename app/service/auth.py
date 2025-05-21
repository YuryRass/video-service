import datetime as dt
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Any

from fastapi import Request, Response
from jose import JWTError, jwt

from app.exceptions import (
    IncorrectEmailOrPasswordException,
    IncorrectJWTtokenException,
    JWTtokenExpiredException,
    UserIsNotPresentException,
    UserUnauthorizedException,
)
from app.models.user import User
from app.repository.user import UserRepository
from app.schema.auth import UserAuthSchema
from app.schema.user import UserLoginSchema
from app.settings import Settings


class JWTPayload(StrEnum):
    USER_ID = "user_id"
    EXPIRE = "expire"


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def _get_token(
        self,
        request: Request,
    ) -> str | None:
        """Возвращает токен пользователя по его HTTP запросу."""
        token = request.cookies.get(self.settings.JWT_COOKIE_KEY)
        if not token:
            raise UserUnauthorizedException
        return token

    def generate_access_token(self, user_id: str) -> str:
        """Генерация JWT токена с временем жизни 7 дней."""

        payload = {
            JWTPayload.USER_ID: user_id,
            JWTPayload.EXPIRE: (
                datetime.now(dt.timezone.utc) + timedelta(days=7)
            ).timestamp(),
        }
        encoded_jwt = jwt.encode(
            payload,
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM,
        )
        return encoded_jwt

    async def get_user_from_access_token(
        self,
        request: Request,
    ) -> User:
        try:
            payload: dict[str, Any] = jwt.decode(
                token=self._get_token(request),
                key=self.settings.JWT_SECRET_KEY,
                algorithms=self.settings.JWT_ENCODE_ALGORITHM,
            )
        except JWTError:
            raise IncorrectJWTtokenException

        expire = payload[JWTPayload.EXPIRE]
        if (not expire) or (expire < datetime.now(tz=dt.UTC).timestamp()):
            raise JWTtokenExpiredException

        user_id = payload.get(JWTPayload.USER_ID)
        if not user_id:
            raise UserIsNotPresentException

        user = await self.user_repository.get_user(id=user_id)
        if not user:
            raise UserIsNotPresentException

        return user

    async def login(
        self,
        user_data: UserAuthSchema,
        response: Response,
    ) -> UserLoginSchema:
        user = await self.user_repository.get_user(email=user_data.email)
        self._validate_auth_user(user, user_data.password)
        access_token = self.generate_access_token(user_id=user.id)
        response.set_cookie(
            key=self.settings.JWT_COOKIE_KEY,
            value=access_token,
            httponly=True,
        )
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: User | None, password: str):
        if not user or user.password != password:
            raise IncorrectEmailOrPasswordException

    async def logout(self, response: Response):
        response.delete_cookie(key=self.settings.JWT_COOKIE_KEY)

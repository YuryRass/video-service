from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, get_user_service
from app.models.user import User
from app.schema.user import UserCreateSchema, UserResponseSchema
from app.service.user import UserService

router: APIRouter = APIRouter(tags=["Users"])


@router.post("/register", summary="Регистрация пользователя")
async def user_register(
    user_data: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
) -> None:
    """Регистрация пользователя."""
    await user_service.register(user_data)


@router.get(
    "/me",
    summary="Информация о пользователе",
    response_model=UserResponseSchema,
)
async def read_users_me(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserResponseSchema:
    """Вывод инфорации о текущем пользователе."""
    return await user_service.read_users_me(current_user)

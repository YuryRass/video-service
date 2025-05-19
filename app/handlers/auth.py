from fastapi import APIRouter, Depends, Response

from app.dependencies import get_auth_service
from app.schema.auth import UserAuthSchema
from app.schema.user import UserLoginSchema
from app.service.auth import AuthService

router: APIRouter = APIRouter(tags=["Users & auth"])


@router.post(
    "/login",
    summary="Вход на сайт",
    response_model=UserLoginSchema,
)
async def login_user(
    response: Response,
    user_data: UserAuthSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserLoginSchema:
    """Вход пользователя на сайт."""
    return await auth_service.login(user_data, response)


@router.post("/logout", summary="Выход из сайта")
async def logout_user(
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    """Выход пользователя."""
    await auth_service.logout(response)

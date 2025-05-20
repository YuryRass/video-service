from app.handlers.auth import router as auth_router
from app.handlers.user import router as user_router
from app.handlers.video import router as video_router

routers = (
    auth_router,
    user_router,
    video_router,
)

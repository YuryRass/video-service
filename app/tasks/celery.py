from celery import Celery

from app.settings import get_settings

celery_app = Celery(
    "tasks",
    broker=get_settings().redis_url,
    include=["app.tasks.generate_hls"],
    backend="rpc://",
)

import urllib.parse
from pathlib import Path
from urllib.parse import urljoin

from app.logger import logger
from app.settings import get_settings
from app.tasks.celery import celery_app

settings = get_settings()


@celery_app.task
def generate_hls(url: str, video_id: int) -> None:
    """Генерация HLS-плейлиста."""
    try:
        logger.info("Генерация HLS-плейлиста...")
        parsed_url = urllib.parse.urlparse(url)

        new_path = f"/hls/{video_id}.m3u8"

        hls_url = urllib.parse.urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                new_path,
                parsed_url.params,
                parsed_url.query,
                parsed_url.fragment,
            )
        )

        segments = [urljoin(hls_url, f"segment{it}.ts") for it in range(1, 6)]
        playlist_content = "#EXTM3U\n" + "\n".join(
            [f"#EXTINF:10,\n{segment}" for segment in segments]
        )

        playlist_path = Path(settings.LOCAL_PATH_TO_HLS)
        playlist_path.mkdir(exist_ok=True)
        playlist_path = playlist_path.joinpath(f"{video_id}.m3u8")
        with open(playlist_path, "w") as f:
            f.write(playlist_content)
        logger.info(f"Сгенерирован новый плейлист: {playlist_path}")
    except Exception as ex:
        logger.error(f"Ошибка в генерации: {ex}", exc_info=True)
        raise

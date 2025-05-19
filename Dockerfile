FROM python:3.12-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /video-service

RUN pip install poetry

COPY poetry.lock pyproject.toml /video-service/

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . /video-service

RUN chmod +x celery_run.sh

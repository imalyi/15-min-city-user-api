from celery import Celery
from api.config import config


celery = Celery(
    "tasks",
    broker=config.REDIS_URL,
    backend=config.REDIS_URL,
    include=["api.tasks.tasks"],
)


celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

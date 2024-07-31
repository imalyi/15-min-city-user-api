from celery import Celery
from api.config import config


celery = Celery(
    "tasks",
    broker=config.REDIS_URL,
    include=["api.tasks.tasks"],
)

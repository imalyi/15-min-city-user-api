from celery import Celery
from api.config import config


celery = Celery(
    "tasks",
    broker="redis://:@node:6379",
    include=["api.tasks.tasks"],
)

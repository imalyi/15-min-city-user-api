from celery import Celery
import os


celery_app = Celery(
    'heatmap_worker',
    broker=os.environ.get("CELERY_BROKER_URL", "redis://node:5123/0"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://node:5123/0")
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

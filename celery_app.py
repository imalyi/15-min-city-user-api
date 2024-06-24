from celery import Celery
import os
from typing import List
from database.schemas import Category
from database.mongo_database import MongoDatabase
import geojson
import redis
from report_generator.report import Report

redis_client = redis.StrictRedis.from_url(os.getenv('REDIS_CACHE', "redis://192.168.0.105:5123/5"), decode_responses=True)

celery_app = Celery(
    '15min_worker',
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

@celery_app.task
def generate_heatmap_task(categories, *args, **kwargs):
   return 1


@celery_app.task
def generate_report_task(address, max_distance, *args, **kwargs):
    r = Report(address, max_distance)
    return r.report

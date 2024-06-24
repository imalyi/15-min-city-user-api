from fastapi import APIRouter
from celery_app import generate_report_task
import redis
import os
import json
from fastapi import Path, Query
import logging

router = APIRouter()

redis_client = redis.StrictRedis.from_url(os.getenv('REDIS_CACHE', "redis://192.168.0.105:5123/1"), decode_responses=True)
logging.basicConfig(level=logging.INFO)


def generate_cache_key(address: str, max_distance: int) -> str:
    return json.dumps({'address': address, 'max_distance': max_distance})


@router.get('/{address}/', status_code=202)
async def get_report(address: str = Path(...), max_distance: int = Query(1400)):
    task = generate_report_task.delay(address, max_distance)
    logging.info(f"Task created with ID: {task.id}")
    return {"task_id": task.id}

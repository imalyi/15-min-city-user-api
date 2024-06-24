from database.schemas import Category
from fastapi import Depends
from fastapi import APIRouter
from database.report_model import MongoDatabase
from database.get_database import get_database
from celery_app import celery_app
import redis
from fastapi import FastAPI, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import List
from celery.result import AsyncResult
from celery_app import celery_app
from database.mongo_database import MongoDatabase
from database.schemas import Category
from celery_app import generate_heatmap_task
import json
import os

router = APIRouter()

redis_client = redis.StrictRedis.from_url(os.getenv('REDIS_CACHE', "redis://192.168.0.105:5123/1"), decode_responses=True)

def generate_cache_key(categories: List[dict]) -> str:
    sorted_categories = sorted(categories, key=lambda x: (x['main_category'], x['category']))
    return json.dumps(sorted_categories)


@router.post("/", status_code=202)
async def generate_heatmap(categories: List[Category]):
    categories_dict = [category.model_dump() for category in categories]
    cache_key = generate_cache_key(categories_dict)
    cached_task_id = redis_client.get(cache_key)
    if cached_task_id:
        return {"task_id": cached_task_id}
    task = generate_heatmap_task.delay(categories_dict)
    redis_client.set(cache_key, task.id)    
    return {"task_id": task.id}


@router.get("/task_status/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)

    if task_result.state == 'PENDING':
        return {"status": "pending", "result": None}
    elif task_result.state == 'FAILURE':
        return {"status": "failure", "result": str(task_result.info)}
    elif task_result.state == 'SUCCESS':
        return {"status": "success", "result": task_result.result}

    return {"status": task_result.state, "result": None}
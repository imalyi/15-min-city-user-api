from database.model import Category
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
from database.model import Category
from celery_app import generate_heatmap_task
import json
import os

router = APIRouter()

# Initialize Redis client using connection string
redis_client = redis.StrictRedis.from_url(os.getenv('REDIS_CACHE', "redis://192.168.0.105:5123/5"), decode_responses=True)

def generate_cache_key(categories: List[dict]) -> str:
    # Sort the categories list based on the name and value
    sorted_categories = sorted(categories, key=lambda x: (x['name'], x['value']))
    # Convert the sorted list to a JSON string to use as the cache key
    return json.dumps(sorted_categories)



@router.get("/")
async def generate_heatmap(categories: List[Category], background_tasks: BackgroundTasks, database: MongoDatabase = Depends(get_database)):
    categories_dict = [category.dict() for category in categories]
    # Generate cache key from sorted categories
    cache_key = generate_cache_key(categories_dict)
    
    # Check if the result is already in the cache
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return {"status": "success", "result": json.loads(cached_result)}
    
    # If not in cache, trigger the Celery task
    task = generate_heatmap_task.delay(categories_dict)
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
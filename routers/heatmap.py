from database.model import Category
from fastapi import Depends
from fastapi import APIRouter
from database.report_model import MongoDatabase
from database.get_database import get_database
from routers.celery_app import celery_app

from fastapi import FastAPI, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import List
from celery.result import AsyncResult
from routers.celery_app import celery_app
from database.mongo_database import MongoDatabase
from database.model import Category
from .tasks import generate_heatmap_task

router = APIRouter()


@router.post("/")
async def generate_heatmap(categories: List[Category], background_tasks: BackgroundTasks, database: MongoDatabase = Depends(get_database)):
    task = generate_heatmap_task.delay(categories.model_dump_json())
    return {"task_id": task.id}
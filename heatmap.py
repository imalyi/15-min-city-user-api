from database.model import Category
from fastapi import Depends
from fastapi import APIRouter
from database.report_model import MongoDatabase
from database.get_database import get_database
from celery_app import celery_app

from fastapi import FastAPI, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import List
from celery.result import AsyncResult
from celery_app import celery_app
from database.mongo_database import MongoDatabase
from database.model import Category
from celery_app import generate_heatmap_task

router = APIRouter()


@router.post("/")
async def generate_heatmap(categories: List[Category], background_tasks: BackgroundTasks, database: MongoDatabase = Depends(get_database)):
    categories = [category.model_dump() for category in categories]
    task = generate_heatmap_task.delay(categories)
    return {"task_id": task.id}
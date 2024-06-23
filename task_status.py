from fastapi import APIRouter
from celery_app import generate_report_task
import redis
import os
from typing import List
import json
from celery.result import AsyncResult
from fastapi import Path, Query

router = APIRouter()


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)

    if task_result.state == 'PENDING':
        return {"status": "pending", "result": None}
    elif task_result.state == 'FAILURE':
        return {"status": "failure", "result": str(task_result.info)}
    elif task_result.state == 'SUCCESS':
        return {"status": "success", "result": task_result.result}

    return {"status": task_result.state, "result": None}
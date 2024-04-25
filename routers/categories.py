import logging
from fastapi import Depends
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from database.mongo_database import MongoDatabase
from database.get_database import get_database
from models.report import Categories
from typing import List, Dict

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/")
async def get_categories(partial_name: str = None, database: MongoDatabase = Depends(get_database)):
    res = {}
    for category, sub_categories in database.get_categories(partial_name).items():
        res[category] = []
        for sub_category in sub_categories:
            res[category].append({'name': sub_category})
    return res
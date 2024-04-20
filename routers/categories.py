import logging
from fastapi import Depends
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from database.mongo_database import MongoDatabase
from database.get_database import get_database
from models.report import Categories
from typing import List

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/")
async def get_categories(database: MongoDatabase = Depends(get_database)):
    return Categories(categories=database.get_categories())

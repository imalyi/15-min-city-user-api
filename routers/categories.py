import logging
from fastapi import Depends
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from database.mongo_database import MongoDatabase
from database.get_database import get_database

logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get("/")
async def get_categories(partial_name: str = None, database: MongoDatabase = Depends(get_database)):
    return database.get_categories(partial_name)

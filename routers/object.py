import logging
from fastapi import Depends
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from database.mongo_database import MongoDatabase
from database.get_database import get_database
from models.report import Objects

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/")
async def get_objects(partial_name: str = None, database: MongoDatabase = Depends(get_database)) -> Objects:
    res = {
        'objects': database.search_object_by_partial_name(partial_name),
        'addresses': database.search_by_partial_name(partial_name)
    }
    return res

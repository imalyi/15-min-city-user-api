import logging
from fastapi import Depends
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from database.mongo_database import MongoDatabase


logging.basicConfig(level=logging.INFO)

app.add_middleware(middleware_class=CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

router = APIRouter()


def get_database():
    return MongoDatabase()


@router.get("/")
async def get_categories(partial_name: str = None, database: MongoDatabase = Depends(get_database)):
    return database.get_categories(partial_name)

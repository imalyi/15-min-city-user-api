import logging
from fastapi import Depends
from fastapi import APIRouter
from database.mongo_database import MongoDatabase
from database.get_database import get_database
from fastapi import FastAPI, HTTPException

router = APIRouter()


@router.get("/")
async def get_address(name: str=None, database: MongoDatabase = Depends(get_database)):
    results = database.search_by_partial_name(name)
    return results

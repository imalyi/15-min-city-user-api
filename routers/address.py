import logging
from fastapi import Depends
from fastapi import APIRouter
from database.report_model import MongoDatabase
from database.get_database import get_database
from fastapi import FastAPI, HTTPException
from database.model import AddressIn, AddressOut
from typing import List
from database.es import fuzzy_search
import os


router = APIRouter()


def get_search_engine(name: str):
    try:
        search_engine = os.getenv("SEARCH_ENGINE").lower() 
    except AttributeError:
        search_engine = 'mongo'
        
    if search_engine == 'mongo':
        return MongoDatabase().search_by_partial_name(name)
    if search_engine == 'opensearch':
        return fuzzy_search(name)

@router.get("/")
async def get_address(q: AddressIn = Depends(), database: MongoDatabase = Depends(get_database)) -> List[str]:
    results = get_search_engine(q.name)
    return results

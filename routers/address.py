import logging
from fastapi import Depends
from fastapi import APIRouter
from database.report_model import MongoDatabase
from database.get_database import get_database
from fastapi import FastAPI, HTTPException
from database.model import AddressIn, AddressOut
from typing import List

router = APIRouter()

@router.get("/")
async def get_address(q: AddressIn = Depends(), database: MongoDatabase = Depends(get_database)) -> List[str]:
    results = database.search_by_partial_name(q.name)
    return results

from fastapi import Depends
from fastapi import APIRouter
from database.get_database import get_database
from database.mongo_database import MongoDatabase
from database.schemas import AddressIn
from typing import List

router = APIRouter()

@router.get("/")
async def get_address(q: AddressIn = Depends(), database: MongoDatabase = Depends(get_database)) -> List[str]:
    results = database.search_by_partial_name(q.name)
    return results

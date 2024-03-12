from fastapi import Depends
from fastapi import APIRouter, Query
from database.mongo_database import MongoDatabase
from database.get_database import get_database
from fastapi import FastAPI, HTTPException
from main import app
router = APIRouter()


@app.get('/')
async def get_report(address: str, cat: list[str] = Query(...), database: MongoDatabase = Depends(get_database)):
    data = database.get_report(address, cat)
    if not data:
        raise HTTPException(status_code=404, detail="Address not found")
    return data

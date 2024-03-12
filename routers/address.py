import logging
from fastapi import Depends
from fastapi import APIRouter
from database.mongo_database import MongoDatabase
from database.get_database import get_database
from fastapi import FastAPI, HTTPException
from main import app
router = APIRouter()
APP_URL = 'https://api.cityinminutes.me/'


class ReportUrl:
    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return f"{APP_URL}?report={self.address}&cat=joga"

    def __str__(self):
        return f"{APP_URL}?report={self.address}&cat=joga"


@app.get("/")
async def get_address(name: str=None, database: MongoDatabase = Depends(get_database)):
    results = database.search_by_partial_name(name)
    results_with_url = []
    for result in results:
        results_with_url.append(str(ReportUrl(result)))
    if not results_with_url:
        raise HTTPException(status_code=404, detail="Address not found")
    return results_with_url

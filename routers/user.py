import logging
from fastapi import Depends
from fastapi import APIRouter
from database.report_model import MongoDatabase
from database.get_database import get_database
from fastapi import FastAPI, HTTPException
from database.model import AddressIn, UserDataIn, SavedReportsOut
from typing import List
from database.report_model import ReportGenerator

router = APIRouter()

@router.post("/save")
async def save_report(data: UserDataIn):
    ReportGenerator().save(data.model_dump())


@router.get('/load')
async def load_report(secret: str) -> SavedReportsOut:
    return ReportGenerator().load(secret)

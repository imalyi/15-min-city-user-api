from fastapi import Depends
from fastapi import APIRouter, Query
from database.mongo_database import MongoDatabase
from database.get_database import get_database
from fastapi import FastAPI, HTTPException
from .googlemaps_distance_calculator import GoogleMapsDistanceCalculator
from pydantic import BaseModel
from typing import List, Dict, Optional

router = APIRouter()


class Report(BaseModel):
    address: str
    cat: List[str]
    custom_names: Optional[List[Dict[str, str]]] = []
    custom_addresses: Optional[List[str]] = []


@router.post('/')
async def get_report(report: Report, database: MongoDatabase = Depends(get_database)):
    data = database.get_report(report.address, report.cat, [{}])
    gmaps = GoogleMapsDistanceCalculator(from_=report.address)
    data['custom'] = {}
    for address in report.custom_addresses:
        data['custom'][address] = gmaps.calc(to=address)
    if not data:
        raise HTTPException(status_code=404, detail="Address not found")
    return data

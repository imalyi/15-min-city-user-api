from fastapi import Depends
from fastapi import APIRouter
from database.mongo_database import MongoDatabase
from database.get_database import get_database
from fastapi import HTTPException
from .googlemaps_distance_calculator import GoogleMapsDistanceCalculator
from pydantic import BaseModel
from typing import List, Dict, Optional
from models.report import ReportOut

router = APIRouter()


class Report(BaseModel):
    address: str
    categories: Optional[List[Dict]] = []
    requested_objects: Optional[List[Dict]] = []
    requested_addresses: Optional[List] = []


@router.post('/')
async def get_report(report: Report, database: MongoDatabase = Depends(get_database)):
    data = database.get_report(report.address, report.categories, report.requested_objects, report.requested_addresses)
    gmaps = GoogleMapsDistanceCalculator(from_=report.address)
    for address in report.requested_addresses:
        if data['custom_addresses'][address]:
            data['custom_addresses'][address]['commute_time'] = gmaps.calc(to=address)
    return data

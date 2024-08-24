from collections import namedtuple
from fastapi import APIRouter, File, HTTPException, UploadFile
from sqlalchemy.orm import exc
from api.pois.dao import POIDAO
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends
from typing import List
from api.pois.categories.router import router as categories_router
from api.pois.schemas import POI, POICreate, POI, POIFilter
import json
from fastapi_filter import FilterDepends
from api.exceptions import DuplicateEntryException
from api.pois.mevo_stops import MevoStops
from api.addresses.dao import AddressDAO
from api.pois.stops import Stops


router = APIRouter(prefix="/pois", tags=["Points of interest"])
router.include_router(categories_router)


@router.get("/", status_code=200, response_model=List[POI])
async def get_all_pois(
    user: User = Depends(current_active_user),
    filters: POIFilter = FilterDepends(POIFilter),
):
    return await POIDAO.find_all(objects_filter=filters)


@router.post("/", status_code=201, response_model=None)
async def create_pois(
    poi_data: POICreate, user: User = Depends(current_admin_user)
):
    try:
        await POIDAO.insert_data(poi_data.model_dump())
    except DuplicateEntryException as err:
        raise HTTPException(409, str(err))


@router.get("/{poi_id}", status_code=200, response_model=POI)
async def get_poi(poi_id: int, user: User = Depends(current_admin_user)):
    return await POIDAO.find_by_id(poi_id)


@router.post("/from_file", status_code=200, response_model=int)
async def create_pois_from_file(
    file: UploadFile = File(...), user: User = Depends(current_admin_user)
):
    content = await file.read()
    content = json.loads(content)
    i = 0
    for poi in content:
        try:
            poi = POICreate.model_validate(poi)
            await create_pois(poi, user)
            i += 1
        except Exception as err:
            print(err)
    return len(content) - i


@router.post("/update_mevo_stops/{city}", status_code=200)
async def update_mevo_stops(
    city: str, user: User = Depends(current_admin_user)
):
    mevo_stops = MevoStops(city)
    for stop in mevo_stops:
        point = namedtuple("Point", ["lat", "lon"])
        point.lat = stop.lat
        point.lon = stop.lon
        stop_address = await AddressDAO.find_by_point(point)
        stop_model = POICreate(name=stop.name, address_id=stop_address[0].id)
        await create_pois(stop_model, user)


@router.post("/update_stops/{stop_type}/{city}")
async def update_stops(
    stop_type: str, city: str, user: User = Depends(current_admin_user)
):
    stops = Stops(city=city, stop_type=stop_type)
    for stop in stops:
        print(stop)

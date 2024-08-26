from collections import namedtuple

from fastapi.routing import APIRoute
from geoalchemy2 import exc
from sqlalchemy.engine import create
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import APIRouter, Depends
from typing import List
from api.pois.categories.router import router as categories_router
from api.pois.dao import POIDAO
from api.pois.categories.router import attach_poi_to_category
from api.pois.schemas import POI, POICreate, POI, POIFilter
from api.category_collections.categories.dao import CategoryDAO
from fastapi_filter import FilterDepends
from api.exceptions import DuplicateEntryException
from api.pois.mevo_stops import MevoStops
from api.addresses.dao import AddressDAO
from api.pois.stops import Stops
from api.category_collections.categories.schemas import CategoryFilter
from api.exceptions import DuplicateEntryException


router = APIRouter(prefix="/stops")


async def create_data(*, source, category: str):
    for poi in source:
        point = namedtuple("Point", ["lat", "lon"])
        point.lat = poi.lat
        point.lon = poi.lon
        poi_address = await AddressDAO.find_by_point(point)
        poi_category = await CategoryDAO.find_one_or_none(
            order_by=None, title=category
        )
        poi_model = POICreate(name=poi.name, address_id=poi_address[0].id)
        try:
            poi = await POIDAO.insert_data(poi_model.model_dump())
            await attach_poi_to_category(poi.id, poi_category.id)
        except DuplicateEntryException:
            continue


@router.post("/mevo", status_code=200)
async def update_mevo_stops(user: User = Depends(current_admin_user)):
    for city in ["Gdańsk", "Sopot", "Gdynia"]:
        source = MevoStops(city=city)
        await create_data(source=source, category="MEVO bikes")


@router.post("/update_stops/{stop_type}/{city}")
async def update_stops(
    stop_type: str, city: str, user: User = Depends(current_admin_user)
):
    stops = Stops(city=city, stop_type=stop_type)
    for stop in stops:
        print(stop)

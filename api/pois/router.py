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

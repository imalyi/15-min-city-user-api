from fastapi import APIRouter
from api.pois.schemas import POICreate, POI, POIAddress, POICategory
from api.addresses.schemas import Address
from api.category_collections.categories.schemas import Category
from api.pois.dao import POIDAO
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends
from typing import List

router = APIRouter(prefix="/pois", tags=["Points of interest"])


@router.get("/", status_code=200, response_model=List[POI])
async def get_all_pois(user: User = Depends(current_active_user)):
    return await POIDAO.find_all()


@router.post("/", status_code=201, response_model=int)
async def create_pois(
    poi_data: POICreate, user: User = Depends(current_admin_user)
):
    return await POIDAO.insert_data(poi_data.model_dump())


@router.post(
    "/{poi_id}/categories/{category_id}",
    status_code=204,
)
async def attach_poi_to_category(
    poi_id: int, category_id: int, user: User = Depends(current_admin_user)
):
    await POIDAO.connect_to_category(poi_id, category_id)


@router.post(
    "/{poi_id}/addresses/{address_id}",
    status_code=204,
)
async def attach_poi_to_address(
    poi_id: int, address_id: int, user: User = Depends(current_admin_user)
):
    await POIDAO.connect_to_address(poi_id, address_id)


@router.get("/{poi_id}", status_code=200, response_model=POI)
async def get_poi(poi_id: int, user: User = Depends(current_active_user)):
    return await POIDAO.find_by_id(poi_id)


@router.get(
    "/{poi_id}/categories/", status_code=200, response_model=list[Category]
)
async def get_poi_categories(
    poi_id: int, user: User = Depends(current_admin_user)
):
    return await POIDAO.get_poi_categories(poi_id)


@router.get(
    "/{poi_id}/addresses/", status_code=200, response_model=list[Address]
)
async def get_poi_addresses(
    poi_id: int, user: User = Depends(current_admin_user)
):
    return await POIDAO.get_poi_addresses(poi_id)

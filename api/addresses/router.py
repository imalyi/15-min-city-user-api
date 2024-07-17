from fastapi import APIRouter
from typing import List
from geoalchemy2 import WKTElement
from api.addresses.dao import AddressDAO
from api.addresses.schemas import Address
from fastapi import Query
from api.addresses.schemas import AddressCreate
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", status_code=201, response_model=int)
async def create_address(
    new_address: AddressCreate, user: User = Depends(current_admin_user)
):
    data = new_address.model_dump()
    data["geometry"] = WKTElement(new_address.geometry.wkt, srid=4326)
    return await AddressDAO.insert_data(data)


@router.get("/", status_code=200, response_model=List[Address])
async def get_all_addresses(
    partial_name: str = Query(None), user: User = Depends(current_active_user)
):
    if partial_name:
        return await AddressDAO.find_by_partial_name(partial_name)
    return await AddressDAO.find_all()


@router.get("/{address_id}", status_code=200, response_model=Address)
async def get_address_by_id(
    address_id: int, user: User = Depends(current_admin_user)
):
    return await AddressDAO.find_by_id(address_id)

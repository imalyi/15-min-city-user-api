from fastapi import APIRouter, UploadFile, File
from typing import List
from geoalchemy2 import WKTElement
from api.addresses.dao import AddressDAO
from api.addresses.schemas import Address
from api.addresses.schemas import AddressCreate
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends
from api.addresses.schemas import AddressFilter
from fastapi_filter import FilterDepends
from typing import Union
import json
from api.opensearch import find_address_by_partial_name

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", status_code=201, response_model=Address)
async def create_address(
    new_address: AddressCreate, user: User = Depends(current_admin_user)
):
    data = new_address.model_dump()
    data["geometry"] = WKTElement(new_address.geometry.wkt, srid=4326)
    return await AddressDAO.insert_data(data)


@router.post("/from_file", status_code=201, response_model=int)
async def create_addresses_from_file(
    file: UploadFile = File(...), user: User = Depends(current_admin_user)
):
    content = await file.read()
    content = json.loads(content)
    i = 0
    for address in content:
        try:
            address = AddressCreate.model_validate(address)
            result = await create_address(address, user)
            i += 1
        except Exception as err:
            print(err, address)
    return len(content) - i


@router.get(
    "/", status_code=200, response_model=Union[List[Address], Address, None]
)
async def get_all_addresses(
    filters: AddressFilter = FilterDepends(AddressFilter),
    user: User = Depends(current_active_user),
):
    if filters.lon and filters.lat:
        return await AddressDAO.find_by_point(filters)
    if filters.full_address__ilike:
        return find_address_by_partial_name(filters.full_address__ilike)
    return await AddressDAO.find_all(filters)


@router.get("/{address_id}", status_code=200, response_model=Address)
async def get_address_by_id(
    address_id: int, user: User = Depends(current_admin_user)
):
    return await AddressDAO.find_by_id(address_id)

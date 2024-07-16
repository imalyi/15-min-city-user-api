from fastapi import APIRouter
from typing import List
from geoalchemy2 import WKTElement
from api.addresses.dao import AddressDAO
from api.addresses.schemas import Address
from fastapi import Query
from api.addresses.schemas import AddressCreate

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", status_code=201, response_model=int)
async def create_address(new_address: AddressCreate):
    data = new_address.model_dump()
    data["geometry"] = WKTElement(new_address.geometry.wkt, srid=4326)
    return await AddressDAO.insert_data(data)


@router.get("/", status_code=200, response_model=List[Address])
async def get_all_addresses(partial_name: str = Query(None)):
    if partial_name:
        return await AddressDAO.find_by_partial_name(partial_name)
    return await AddressDAO.find_all()


@router.get("/{address_id}", status_code=200, response_model=Address)
async def get_address_by_id(address_id: int):
    return await AddressDAO.find_by_id(address_id)

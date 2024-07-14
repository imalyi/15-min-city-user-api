from fastapi import APIRouter
from typing import List
from api.schemas.address import AddressCreate
from geoalchemy2 import WKTElement
from api.addresses.dao import AddressDAO
from api.addresses.schemas import Address
from fastapi import Query

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", status_code=204)
async def create_address(new_address: AddressCreate):
    data = new_address.model_dump()
    data["geometry"] = WKTElement(new_address.geometry.wkt, srid=4326)
    await AddressDAO.insert_data(data)


@router.get("/", status_code=200, response_model=List[Address])
async def get_all_addresses(partial_name: str = Query(...)):
    if partial_name:
        return await AddressDAO.find_by_partial_name(partial_name)
    return await AddressDAO.find_all()


@router.get("/{address_id}", status_code=200, response_model=Address)
async def get_address_by_id(address_id: int):
    return await AddressDAO.find_by_id(address_id)


@router.get(
    "/by_partial_name/{partial_name}",
    status_code=200,
    response_model=List[Address],
)
async def get_address_by_partial_name(partial_name: str):
    return await AddressDAO.find_by_partial_name(partial_name)

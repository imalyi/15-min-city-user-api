from fastapi import APIRouter, HTTPException
from api.database import address_table

from api.schemas.address import Address, AddressCreate
from api.database import database

router = APIRouter()
# https://camillovisini.com/coding/abstracting-fastapi-services read this about dals and something else


@router.get("/", status_code=200, response_model=list[Address])
async def get_all_addresses():
    query = address_table.select()
    return await database.fetch_all(query=query)


@router.post("/", status_code=201, response_model=Address)
async def create_address(address: AddressCreate):
    data = address.model_dump()
    query = address_table.select().where(address_table.c.street == data["street"])
    address = await database.fetch_one(query=query)
    if not address:
        query = address_table.insert().values(data)
        address_id = await database.execute(query=query)
        return {**data, "id": address_id}
    return address


@router.get("/{address_id}", status_code=200, response_model=Address)
async def get_address(address_id: int):
    query = address_table.select().where(address_table.c.id == address_id)
    result = await database.fetch_one(query=query)
    if not result:
        raise HTTPException(404, f"Address with id {address_id} not exists")

    return result

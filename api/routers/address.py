from fastapi import APIRouter, HTTPException
from api.database import address_table

from api.schemas.address import Address, AddressCreate
from api.database import database
from geoalchemy2 import WKTElement

router = APIRouter()


def insert_percent_after_each_char(input_string):
    # Join each character in the input string with '%'
    return "%".join(input_string) + "%"


@router.get("/", status_code=200, response_model=list[Address])
async def get_all_addresses():
    query = address_table.select()
    return await database.fetch_all(query=query)


@router.get("/{street}", status_code=200, response_model=list[Address])
async def get_address_by_partial_name(street: str):
    query = address_table.select().where(
        address_table.c.full_address.ilike(
            insert_percent_after_each_char(street)
        )
    )
    return await database.fetch_all(query=query)


@router.post("/", status_code=204)
async def create_address(address: AddressCreate):
    query = address_table.select().where(
        address_table.c.street == address.street
    )
    existing_addres = await database.fetch_one(query=query)
    if existing_addres:
        raise HTTPException(409, f"Adress exists")
    query = address_table.insert().values(
        street=address.street,
        city=address.city,
        postcode=address.postcode,
        geometry=WKTElement(address.geometry.wkt, srid=4326),
    )
    await database.execute(query=query)


@router.get("/{address_id}", status_code=200, response_model=Address)
async def get_address(address_id: int):
    query = address_table.select().where(address_table.c.id == address_id)
    result = await database.fetch_one(query=query)
    if not result:
        raise HTTPException(404, f"Address with id {address_id} not exists")
    return result

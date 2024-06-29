"""
POI (Points of Interest) Management Module
This module provides APIs for managing POIs.
It also provides APIs for attaching POIs to categories and addresses.
"""

from fastapi import APIRouter, HTTPException
from api.schemas.poi import POICreate, POI

from api.database import database
from api.database import poi_table
from api.routers.category import get_category
from api.routers.address import get_address

from api.database import poi_category_table
from api.schemas.category import Category
from api.schemas.address import Address
from api.database import poi_address_table


router = APIRouter()


async def is_poi_exists(name: str):
    """
    Check if a POI with the given name exists

    Args:
    name (str): The name of the POI to check

    Returns:
    bool: True if the POI exists, False otherwise
    """
    query = poi_table.select().where((poi_table.c.name == name))
    result = await database.fetch_one(query=query)
    return result


@router.get("/", status_code=200)
async def get_all_pois():
    """
    Get all POIs

    Returns:
    list: A list of all POIs
    """
    query = poi_table.select()
    return await database.fetch_all(query=query)


@router.post("/", status_code=201)
async def create_pois(poi_data: POICreate):
    """
    Create a new POI

    Args:
    poi_data (POICreate): The data for the new POI

    Returns:
    int: The ID of the created POI

    Raises:
    HTTPException: If a POI with the same name already exists
    """
    data = poi_data.model_dump()
    poi = await is_poi_exists(data["name"])
    if poi:
        raise HTTPException(409, f"POI with name  {data['name']} exists")
    query = poi_table.insert().values(data)
    return await database.execute(query=query)


@router.post("/{poi_id}/categories/{category_id}", status_code=201)
async def attach_poi_to_category(poi_id: int, category_id: int):
    """
    Attach a POI to a category

    Args:
    poi_id (int): The ID of the POI
    category_id (int): The ID of the category

    Returns:
    None
    """
    _ = await get_poi(poi_id)
    _ = await get_category(category_id)
    query = poi_category_table.insert().values(
        {"category_id": category_id, "poi_id": poi_id}
    )
    await database.execute(query=query)


@router.get("/{poi_id}", status_code=200, response_model=POI)
async def get_poi(poi_id: int):
    """
    Get a POI by ID

    Args:
    poi_id (int): The ID of the POI

    Returns:
    POI: The POI with the given ID

    Raises:
    HTTPException: If the POI does not exist
    """
    query = poi_table.select().where(poi_table.c.id == poi_id)
    result = await database.fetch_one(query=query)
    if not result:
        raise HTTPException(404, f"POI with id {poi_id} not exists")
    return result


@router.get(
    "/{poi_id}/categories/", status_code=200, response_model=list[Category]
)
async def get_poi_categories(poi_id: int):
    """
    Get the categories of a POI

    Args:
    poi_id (int): The ID of the POI

    Returns:
    list[Category]: A list of categories associated with the POI
    """
    query = poi_category_table.select().where(
        poi_category_table.c.poi_id == poi_id
    )
    poi_categories = await database.fetch_all(query=query)
    categories_obj = []
    for poi_category in poi_categories:
        categories_obj.append(await get_category(poi_category.category_id))

    return categories_obj


@router.get(
    "/{poi_id}/addresses/", status_code=200, response_model=list[Address]
)
async def get_poi_addresses(poi_id: int):
    """
    Get the addresses of a POI

    Args:
    poi_id (int): The ID of the POI

    Returns:
    list[Address]: A list of addresses associated with the POI
    """
    query = poi_address_table.select().where(
        poi_address_table.c.poi_id == poi_id
    )
    poi_addresses = await database.fetch_all(query=query)
    address_obj = []
    for poi_address in poi_addresses:
        address_obj.append(await get_address(poi_address.address_id))
    return address_obj


@router.post("/{poi_id}/addresses/{address_id}", status_code=201)
async def attach_poi_to_address(poi_id: int, address_id: int):
    """
    Attach a POI to an address

    Args:
    poi_id (int): The ID of the POI
    address_id (int): The ID of the address

    Returns:
    None

    Raises:
    HTTPException: If the POI does not exist
    """
    _ = await get_poi(poi_id)
    _ = await get_address(address_id)
    query = poi_address_table.insert().values(
        {"address_id": address_id, "poi_id": poi_id}
    )
    await database.execute(query=query)

import datetime
from operator import add
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from geoalchemy2 import WKTElement
from pyrosm import get_data
from api.addresses.dao import AddressDAO
from api.addresses.schemas import Address
from api.addresses.schemas import AddressCreate
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends
from api.addresses.schemas import AddressFilter, AddressUpdate
from fastapi_filter import FilterDepends
from typing import Union
import json
from api.opensearch import find_address_by_partial_name
from api.exceptions import DuplicateEntryException
from api.addresses.osm_residential_buildings import (
    OSMResidentialBuildings,
    Report,
)
from pyrosm import OSM, get_data
from pydantic import ValidationError

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", status_code=201, response_model=Address)
async def create_address(
    new_address: AddressCreate, user: User = Depends(current_admin_user)
):
    "Creates address if not exists or update mofified_at time"
    data = new_address.model_dump()
    data["geometry"] = WKTElement(new_address.geometry.wkt, srid=4326)
    try:
        return await AddressDAO.insert_data(data)
    except DuplicateEntryException as e:
        existing_address = await AddressDAO.find_one_or_none(
            order_by=None,
            city=data["city"],
            street_name=data["street_name"],
            house_number=data["house_number"],
        )
        await AddressDAO.update_data(
            existing_address.id, modified_at=datetime.datetime.now()
        )


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


@router.patch("/{address_id}", response_model=Address)
async def update_category_collection(
    address_id: int,
    address_update: AddressUpdate,
    user: User = Depends(current_admin_user),
):

    existing_address = await AddressDAO.find_by_id(address_id)
    if not existing_address:
        raise HTTPException(
            status_code=404,
            detail="Category collection not found",
        )

    update_data = address_update.model_dump(exclude_unset=True)
    if update_data:
        updated_collection = await AddressDAO.update_data(
            address_id, update_data
        )
        return updated_collection
    else:
        raise HTTPException(
            status_code=400,
            detail="No valid fields to update",
        )


@router.post("/{city}")
async def update_all_addressess(
    city: str, user: User = Depends(current_admin_user)
):
    report = Report()
    addresses = OSMResidentialBuildings(osm=OSM(get_data(city)), report=report)

    for address in addresses:
        try:
            address_model = AddressCreate.model_validate(address.to_dict())
            await create_address(address_model, user)
        except HTTPException:
            report.mark_address_exists(address)
            continue
        except ValidationError:
            report.mark_address_as_bad(address)
            continue
    return report.stats

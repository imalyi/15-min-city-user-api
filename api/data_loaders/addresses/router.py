from fastapi import APIRouter
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends
from api.data_loaders.addresses.osm_residential_buildings import (
    OSMResidentialBuildings,
    Report,
)
from pyrosm import OSM, get_data
from api.addresses.schemas import AddressCreate
from api.addresses.router import create_address
from pydantic import ValidationError
from fastapi import HTTPException
import asyncio

router = APIRouter(prefix="/addresses")


@router.post("/{city}")
async def update_all_addressess(
    city: str, user: User = Depends(current_admin_user)
):
    report = Report()
    addresses = OSMResidentialBuildings(city=city, report=report)

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

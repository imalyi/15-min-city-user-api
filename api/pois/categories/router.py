from fastapi import APIRouter
from api.category_collections.categories.schemas import Category
from api.pois.dao import POIDAO
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends

router = APIRouter(
    prefix="/categories", tags=["Points of interest", "POI Categories"]
)


@router.post(
    "/{poi_id}/categories/{category_id}",
    status_code=204,
)
async def attach_poi_to_category(
    poi_id: int, category_id: int, user: User = Depends(current_admin_user)
):
    await POIDAO.connect_to_category(poi_id, category_id)


@router.get(
    "/{poi_id}/categories/", status_code=200, response_model=list[Category]
)
async def get_poi_categories(
    poi_id: int, user: User = Depends(current_admin_user)
):
    return await POIDAO.get_poi_categories(poi_id)

from fastapi import APIRouter, HTTPException
from api.category_collections.schemas import (
    CategoryCollectionCreate,
    CategoryCollection,
)
from api.category_collections.dao import CategoryCollectionsDAO
from typing import List
from api.users.user_manager import (
    current_active_user,
    current_admin_user,
    current_user_optional,
)
from api.users.models import User
from fastapi import Depends
from fastapi_filter import FilterDepends
from api.category_collections.schemas import CategoryCollectionFilter
from api.exceptions.unique import DBException

router = APIRouter(
    prefix="/category-collections", tags=["Category Collections"]
)


@router.get("/", status_code=200, response_model=List[CategoryCollection])
async def get_all_category_collections(
    user: User = Depends(current_user_optional),
    filters: CategoryCollectionFilter = FilterDepends(
        CategoryCollectionFilter
    ),
):
    if not user or not user.is_superuser:
        result = await CategoryCollectionsDAO.find_all(is_hidden=True)
    else:
        result = await CategoryCollectionsDAO.find_all(is_hidden=False)
    result_dto = [
        CategoryCollection.model_validate(row, from_attributes=True)
        for row in result
    ]

    return result_dto


@router.post("/", status_code=201, response_model=CategoryCollection)
async def create_category_collection(
    new_category_collection: CategoryCollectionCreate,
    user: User = Depends(current_admin_user),
):
    try:
        return await CategoryCollectionsDAO.insert_data(
            new_category_collection.model_dump()
        )
    except DBException:
        raise HTTPException(409, "Category collection exists")

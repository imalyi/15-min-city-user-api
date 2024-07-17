from fastapi import APIRouter, HTTPException
from api.category_collections.schemas import (
    CategoryCollectionCreate,
    CategoryCollection,
)
from api.category_collections.dao import CategoryCollectionsDAO
from typing import List
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends


router = APIRouter(
    prefix="/category-collections", tags=["Categories", "Category Collections"]
)


@router.get("/", status_code=200, response_model=List[CategoryCollection])
async def get_all_category_collections(
    user: User = Depends(current_active_user),
):
    result = await CategoryCollectionsDAO.find_all()
    result_dto = [
        CategoryCollection.model_validate(row, from_attributes=True)
        for row in result
    ]

    return result_dto


@router.post("/", status_code=204)
async def create_category_collection(
    new_category_collection: CategoryCollectionCreate,
    user: User = Depends(current_admin_user),
):
    await CategoryCollectionsDAO.insert_data(
        new_category_collection.model_dump()
    )

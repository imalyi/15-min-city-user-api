from fastapi import APIRouter, HTTPException
from api.category_collections.schemas import (
    CategoryCollectionCreate,
    CategoryCollection,
    CategoryCollectionUpdate,
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

from api.exceptions import DuplicateEntryException

router = APIRouter(
    prefix="/category-collections", tags=["Category Collections"]
)


@router.patch("/{collection_id}", response_model=CategoryCollection)
async def update_category_collection(
    collection_id: int,
    category_update: CategoryCollectionUpdate,
    user: User = Depends(current_admin_user),
):

    existing_collection = await CategoryCollectionsDAO.find_by_id(
        collection_id
    )
    if not existing_collection:
        raise HTTPException(
            status_code=404,
            detail="Category collection not found",
        )

    update_data = category_update.dict(exclude_unset=True)
    if update_data:
        updated_collection = await CategoryCollectionsDAO.update_data(
            collection_id, update_data
        )
        return updated_collection
    else:
        raise HTTPException(
            status_code=400,
            detail="No valid fields to update",
        )


@router.get("/", status_code=200, response_model=List[CategoryCollection])
async def get_all_category_collections(
    user: User = Depends(current_user_optional),
    filters: CategoryCollectionFilter = FilterDepends(
        CategoryCollectionFilter
    ),
):
    if not user or not user.is_superuser:
        result = await CategoryCollectionsDAO.find_all(is_hidden=False)
    else:
        result = await CategoryCollectionsDAO.find_all(is_hidden=True)
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
    except DuplicateEntryException:
        raise HTTPException(409, "Category collectiom exists")


# @router.post("/{collection_id}/categories")
# async def create_category_in_collection(
#    collection_id: int,
#    new_category: CategoryCreate,
# user: User = Depends(current_admin_user)
# ):
#    res = await CategoryCollectionsDAO.find_by_id(collection_id)ы

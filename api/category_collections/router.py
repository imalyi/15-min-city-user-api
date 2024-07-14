from fastapi import APIRouter, HTTPException
from api.category_collections.schemas import (
    CategoryCollectionCreate,
    CategoryCollection,
)
from api.category_collections.dao import CategoryCollectionsDAO
from typing import List


router = APIRouter(
    prefix="/category-collections", tags=["Categories", "Category Collections"]
)


@router.get("/", status_code=200, response_model=List[CategoryCollection])
async def get_all_category_collections():
    result = await CategoryCollectionsDAO.find_all()
    result_dto = [
        CategoryCollection.model_validate(row, from_attributes=True)
        for row in result
    ]

    return result_dto


@router.post("/", status_code=204)
async def create_category_collection(
    new_category_collection: CategoryCollectionCreate,
):
    await CategoryCollectionsDAO.insert_data(
        new_category_collection.model_dump()
    )

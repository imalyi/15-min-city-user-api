from fastapi import APIRouter, HTTPException
from api.categories.schemas import CategoryCreate, Category
from api.categories.dao import CategoryDAO
from typing import List

categories_router = APIRouter(prefix="/categories", tags=["Categories"])
category_collections_router = APIRouter(
    prefix="/category-collections", tags=["Categories", "Category Collections"]
)


@categories_router.get("/", status_code=200, response_model=List[Category])
async def get_all_categories():
    return await CategoryDAO.find_all()


@categories_router.get(
    "/{category_id}", status_code=200, response_model=Category
)
async def get_category_by_id(category_id: int):
    return await CategoryDAO.find_by_id(category_id)


@categories_router.post("/", status_code=204)
async def create_category(new_category: CategoryCreate):
    await CategoryDAO.insert_data(new_category.model_dump())

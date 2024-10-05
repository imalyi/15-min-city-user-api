from fastapi import APIRouter, HTTPException
from api.category_collections.categories.schemas import (
    CategoryCreate,
    Category,
    CategoryFilter,
)
from api.category_collections.categories.dao import CategoryDAO
from typing import List
from fastapi_filter import FilterDepends

categories_router = APIRouter(prefix="/categories", tags=["Categories"])
category_collections_router = APIRouter(
    prefix="/category-collections", tags=["Categories", "Category Collections"]
)
from api.users.user_manager import (
    current_active_user,
    current_admin_user,
    current_user_optional,
)
from api.users.models import User
from fastapi import Depends


@categories_router.get("/", status_code=200, response_model=List[Category])
async def get_all_categories(
    filters: CategoryFilter = FilterDepends(CategoryFilter),
    user: User = Depends(current_user_optional),
):
    return await CategoryDAO.find_all(filters)


@categories_router.get(
    "/{category_id}", status_code=200, response_model=Category
)
async def get_category_by_id(
    category_id: int, user: User = Depends(current_user_optional)
):
    category = await CategoryDAO.find_by_id(category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    return category
    

@categories_router.post("/", status_code=201, response_model=Category)
async def create_category(
    new_category: CategoryCreate, user: User = Depends(current_admin_user)
):
    return await CategoryDAO.insert_data(new_category.model_dump())

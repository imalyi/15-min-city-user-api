from fastapi import APIRouter, HTTPException
from api.category_collections.categories.schemas import (
    CategoryCreate,
    Category,
)
from api.category_collections.categories.dao import CategoryDAO
from typing import List
from api.exceptions.unique import DBException


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
from api.exceptions.unique import UniqueConstraintException


@categories_router.get("/", status_code=200, response_model=List[Category])
async def get_all_categories(user: User = Depends(current_admin_user)):
    return await CategoryDAO.find_all()


@categories_router.get(
    "/{category_id}", status_code=200, response_model=Category
)
async def get_category_by_id(
    category_id: int, user: User = Depends(current_admin_user)
):
    return await CategoryDAO.find_by_id(category_id)


@categories_router.post("/", status_code=201, response_model=Category)
async def create_category(
    new_category: CategoryCreate, user: User = Depends(current_admin_user)
):
    try:
        return await CategoryDAO.insert_data(new_category.model_dump())
    except DBException:
        raise HTTPException(409, f"Category with {new_category} exists")

"""
This module defines the API endpoints for managing categories.
"""

from fastapi import APIRouter, HTTPException
from api.schemas.category import CategoryCreate, Category, Preference
from api.database import database
from api.database import category_table, category_collections_table

router = APIRouter()


@router.get("/", status_code=200, response_model=list[Preference])
async def get_all_preferences():
    query = category_collections_table.select()
    return await database.fetch_all(query=query)


@router.get(
    "/{collection_id}/", status_code=200, response_model=list[Category]
)
async def get_categories_from_collection(collection_id: int):
    query = category_table.select().where(
        category_table.c.collection_id == collection_id
    )
    return await database.fetch_all(query=query)


@router.get(
    "/categories/{category_id}", status_code=200, response_model=Category
)
async def get_category(category_id: int):
    """
    Retrieve a specific category by ID.

    Args:
        category_id (int): The ID of the category to retrieve.

    Returns:
        Category: The category object with the specified ID.

    Raises:
        HTTPException: If the category with the given ID is not found.
    """
    query = category_table.select().where(category_table.c.id == category_id)
    category = await database.fetch_one(query=query)
    if not category:
        raise HTTPException(
            404, f"Category with given id {category_id} not found"
        )
    return category


@router.post("/categories/", status_code=201, response_model=Category)
async def create_category(category: CategoryCreate):
    """
    Create a new category.

    Args:
        response (Response): The response object.
        category (CategoryCreate): The category data to create.

    Returns:
        Category: The created category object with its ID.

    Raises:
        HTTPException: If the category already exists.
    """
    data = category.model_dump()
    query = category_table.select().where(
        category_table.c.parent_category == data["parent_category"],
        category_table.c.child_category == data["child_category"],
    )
    if not category:
        query = category_table.insert().values(data)
        category_id = await database.execute(query=query)
        return {**data, "id": category_id}
    raise HTTPException(
        409,
        f"Category {data['parent_category']} {data['child_category']} exists",
    )


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(category_id: int):
    """
    Delete a specific category by ID.

    Args:
        category_id (int): The ID of the category to delete.
    """
    query = category_table.delete().where(category_table.c.id == category_id)
    await database.execute(query=query)


@router.delete("/categories/", status_code=204)
async def delete_all_categories():
    """
    Delete all categories.
    """
    query = category_table.delete()
    await database.execute(query=query)

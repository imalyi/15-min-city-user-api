from fastapi import APIRouter, HTTPException, Response
from api.schemas.category import CategoryCreate, Category
from api.database import database
from api.database import category_table


router = APIRouter()


@router.get("/", status_code=200, response_model=list[Category])
async def get_categories():
    query = category_table.select()
    return await database.fetch_all(query=query)


@router.get("/{category_id}", status_code=200, response_model=Category)
async def get_category(category_id: int):
    query = category_table.select().where(category_table.c.id == category_id)
    category = await database.fetch_one(query=query)
    if not category:
        raise HTTPException(404, f"Category with given id {category_id} not found")
    return category


@router.post("/", status_code=201, response_model=Category)
async def create_category(response: Response, category: CategoryCreate):
    data = category.model_dump()
    query = category_table.select().where(
        category_table.c.parent_category == data["parent_category"],
        category_table.c.child_category == data["child_category"],
    )
    if not category:
        query = category_table.insert().values(data)
        category_id = await database.execute(query=query)
        return {**data, "id": category_id}
    raise HTTPException(409, f"Category {data['parent_category']} {data['child_category']} exists")


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int):
    query = category_table.delete().where(category_table.c.id == category_id)
    await database.execute(query=query)


@router.delete("/", status_code=204)
async def delete_all_categories():
    query = category_table.delete()
    await database.execute(query=query)


@router.put("/")
async def modify_category(category: Category):
    # must return status code 201 if category was created and 204 if updated
    pass

import logging
from fastapi import APIRouter
from database.DALs.category_dal import CategoryDAL
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)

router = APIRouter()


class CategoryCreate(BaseModel):
    main_category: str
    sub_category: str

@router.get("/", status_code=200)
async def get_all_categories():
    return CategoryDAL().get_all_categories()

@router.get("/{id_}", status_code=200)
async def get_category(id_):
    return CategoryDAL().get_category(id_)

@router.post("/", status_code=201)
async def create_category(category_data: CategoryCreate):
    CategoryDAL().create_category(main_category=category_data.main_category, sub_category=category_data.sub_category)
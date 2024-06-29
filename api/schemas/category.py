from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    model_config = ConfigDict()
    parent_category: str
    child_category: str


class Category(CategoryCreate):
    id: int

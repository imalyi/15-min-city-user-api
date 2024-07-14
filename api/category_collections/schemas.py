from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field
from typing import List
from api.categories.schemas import Category


class CategoryCollectionCreate(GlobalModelWithJSONAlias):
    title: str


class CategoryCollection(CategoryCollectionCreate):
    id_: int = Field(alias="id")
    categories: List[Category]

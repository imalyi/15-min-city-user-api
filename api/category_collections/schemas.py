from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field, field_validator
from typing import List, Optional
from api.category_collections.categories.schemas import Category
import re
from fastapi_filter.contrib.sqlalchemy import Filter
from api.category_collections.models import (
    CategoryCollections as CategoryCollectionModel,
)
from datetime import datetime


class CategoryCollectionCreate(GlobalModelWithJSONAlias):
    title: str = Field(min_length=5, max_length=100)
    synonims: Optional[List[str]] = None
    order: int

    @field_validator("title")
    def only_characters_and_spaces(cls, v):
        pattern = re.compile(r"^[A-Za-z, ]*$")
        if bool(pattern.match(v)):
            return v
        raise ValueError(
            "CategoryCollection title can contain only latin characters and spaces"
        )


class CategoryCollection(CategoryCollectionCreate):
    id_: int = Field(alias="id")
    categories: Optional[List[Category]] = None
    created_at: datetime


class CategoryCollectionFilter(Filter):
    title: Optional[str] = None
    title__ilike: Optional[str] = None
    order_by: list[str] = ["title"]

    class Constants(Filter.Constants):
        model = CategoryCollectionModel

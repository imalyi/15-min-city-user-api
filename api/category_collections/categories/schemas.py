from pydantic import Field, field_validator
from api.schemas.global_model import GlobalModelWithJSONAlias
import re
from fastapi_filter.contrib.sqlalchemy import Filter
from api.category_collections.categories.models import (
    Categories as CategoriesModel,
)
from typing import Optional, List

# TODO: use Annotated for title validation


class CategoryCreate(GlobalModelWithJSONAlias):
    title: str = Field(
        min_length=2,
        max_length=100,
    )
    collection_id: int
    is_default: bool
    is_hidden: bool
    order: int = Field(ge=0)
    minimum_subscription_level: int = Field(ge=0)

    @field_validator("title")
    def only_characters_and_spaces(cls, v):
        pattern = re.compile(r"^[A-Za-z, ]*$")
        if bool(pattern.match(v)):
            return v
        raise ValueError(
            "Category title can contain only latin characters and spaces"
        )


class Category(CategoryCreate):
    id_: int = Field(alias="id")


class CategoryFilter(Filter):
    title: Optional[str] = None
    collection_id: Optional[int] = None
    order_by: List[str] = ["title"]

    class Constants(Filter.Constants):
        model = CategoriesModel

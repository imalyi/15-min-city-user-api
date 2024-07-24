from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field, field_validator
from typing import List
from api.category_collections.categories.schemas import Category
import re


class CategoryCollectionCreate(GlobalModelWithJSONAlias):
    title: str = Field(min_length=5, max_length=100)

    @field_validator("title")
    def only_characters_and_spaces(cls, v):
        pattern = re.compile(r"^[A-Za-z ]*$")
        if bool(pattern.match(v)):
            return v
        raise ValueError(
            "CategoryCollection title can contain only latin characters and spaces"
        )


class CategoryCollection(CategoryCollectionCreate):
    id_: int = Field(alias="id")
    categories: List[Category]

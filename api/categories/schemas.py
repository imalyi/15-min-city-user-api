from pydantic import Field
from api.schemas.global_model import GlobalModelWithJSONAlias


class CategoryCreate(GlobalModelWithJSONAlias):
    title: str
    collection_id: int
    is_default: bool
    is_hidden: bool
    order: int


class Category(CategoryCreate):
    id_: int = Field(alias="id")

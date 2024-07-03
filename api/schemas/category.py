from pydantic import ConfigDict, Field, BaseModel
from api.schemas.global_model import GlobalModelWithJSONAlias


class CategoryCreate(GlobalModelWithJSONAlias):
    model_config = ConfigDict()
    title: str
    collection_id: int
    is_default: bool
    is_hidden: bool


class Category(CategoryCreate):
    id_: int = Field(alias="id")


class PreferenceCreate(GlobalModelWithJSONAlias):
    title: str


class Preference(PreferenceCreate):
    id_: int = Field(alias="id")

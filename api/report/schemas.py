from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field
from typing import List


class ReportCreate(GlobalModelWithJSONAlias):
    category_ids: List[int]
    address_id: int = Field(ge=0)
    custom_address_ids: List[int] | None = Field(default=None)
    distance: int = Field(ge=100, le=10000, default=300)

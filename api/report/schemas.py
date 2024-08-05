from click import File
from api.schemas.global_model import GlobalModelWithJSONAlias
from pydantic import Field
from typing import List, Optional


class ReportCreate(GlobalModelWithJSONAlias):
    category_ids: List[int]
    address_id: int = Field(ge=0)
    custom_address_ids: Optional[List[int]] = Field(default=[])
    custom_places_ids: Optional[List[int]] = Field(default=[])
    distance: int = Field(ge=100, le=10000, default=300)

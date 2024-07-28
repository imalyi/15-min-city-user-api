from api.schemas.global_model import GlobalModelWithJSONAlias
import datetime
from typing import List, Optional
from pydantic import Field


class POICreate(GlobalModelWithJSONAlias):
    name: str = Field(min_length=3)
    data: Optional[dict] = None
    address_id: int


class POI(POICreate):
    id: int
    created_at: datetime.datetime
    modified_at: Optional[datetime.datetime] = None

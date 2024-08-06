from api.schemas.global_model import GlobalModelWithJSONAlias
import datetime
from typing import List, Optional
from pydantic import ConfigDict, Field, fields
from fastapi_filter.contrib.sqlalchemy import Filter
from api.pois.models import POI as POIModel


class POICreate(GlobalModelWithJSONAlias):
    name: str = Field(min_length=3)
    address_id: int


class POI(POICreate):
    id: int
    created_at: datetime.datetime
    modified_at: Optional[datetime.datetime] = None


class POIFilter(Filter, GlobalModelWithJSONAlias):
    name__ilike: Optional[str] = Field(default=None, alias="name__ilike")
    order_by: list[str] = ["name"]

    class Constants(Filter.Constants):
        model = POIModel

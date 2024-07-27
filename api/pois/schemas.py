from api.schemas.global_model import GlobalModelWithJSONAlias
import datetime
from typing import List, Optional
from pydantic import Field


class POICreate(GlobalModelWithJSONAlias):
    name: str
    description: Optional[str] = None
    opening_hours: Optional[str] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    place_id_google_api: Optional[str] = None
    price_level: Optional[str] = None
    types: Optional[List[str]] = []


class POI(POICreate):
    id: int
    created_at: datetime.datetime
    modified_at: Optional[datetime.datetime] = None

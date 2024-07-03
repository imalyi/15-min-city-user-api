from pydantic import BaseModel
import datetime


class POICategory(BaseModel):
    created_at: datetime.datetime
    last_seen_at: datetime.datetime | None
    poi_id: int
    category_id: int

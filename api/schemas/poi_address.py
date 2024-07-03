from pydantic import BaseModel
import datetime


class POIAddress(BaseModel):
    created_at: datetime.datetime
    last_seen_at: datetime.datetime | None
    poi_id: int
    address_id: int

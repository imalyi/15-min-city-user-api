from api.schemas.global_model import GlobalModelWithJSONAlias
import datetime


class POICreate(GlobalModelWithJSONAlias):
    name: str


class POI(POICreate):
    id: int


class POIAddress(GlobalModelWithJSONAlias):
    created_at: datetime.datetime
    last_seen_at: datetime.datetime | None
    poi_id: int
    address_id: int


class POICategory(GlobalModelWithJSONAlias):
    created_at: datetime.datetime
    last_seen_at: datetime.datetime | None
    poi_id: int
    category_id: int

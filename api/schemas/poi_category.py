from pydantic import BaseModel
import datetime
from api.schemas.global_model import GlobalModelWithJSONAlias


class POICategory(GlobalModelWithJSONAlias):
    created_at: datetime.datetime
    last_seen_at: datetime.datetime | None
    poi_id: int
    category_id: int

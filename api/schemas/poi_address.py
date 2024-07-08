from pydantic import BaseModel
import datetime
from pydantic import ConfigDict, Field, BaseModel
from api.schemas.global_model import GlobalModelWithJSONAlias


class POIAddress(GlobalModelWithJSONAlias):
    created_at: datetime.datetime
    last_seen_at: datetime.datetime | None
    poi_id: int
    address_id: int

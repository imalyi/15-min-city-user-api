from api.schemas.global_model import GlobalModelWithJSONAlias
import datetime
from typing import List


class POICategory(GlobalModelWithJSONAlias):
    created_at: datetime.datetime
    modified_at: datetime.datetime | None
    poi_id: int
    category_id: int

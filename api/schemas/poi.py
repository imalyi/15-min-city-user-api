from pydantic import BaseModel
from api.schemas.global_model import GlobalModelWithJSONAlias


class POICreate(GlobalModelWithJSONAlias):
    name: str


class POI(POICreate):
    id: int

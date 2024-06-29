from pydantic import BaseModel


class POICreate(BaseModel):
    name: str


class POI(POICreate):
    id: int
